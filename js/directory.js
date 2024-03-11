class directory {
  /**
   * Class constructor with basic chart configuration
   * @param {Object}
   * @param {Array}
   */
  constructor(_config, _data) {
    this.config = {
      parentElement: _config.parentElement,
      containerWidth: _config.containerWidth || 800,
      containerHeight: _config.containerHeight || 1000,
      margin: _config.margin || { top: 25, right: 20, bottom: 20, left: 35 },
      tooltipPadding: _config.tooltipPadding || 15,
    };
    this.data = _data;
    this.initVis();
  }

  /**
   * We initialize scales/axes and append static elements, such as axis titles.
   */
  initVis() {
    let vis = this;
    // Calculate inner chart size. Margin specifies the space around the actual chart.
    vis.width =
      vis.config.containerWidth -
      vis.config.margin.left -
      vis.config.margin.right;

    vis.height = vis.width;
    vis.radius = vis.width / 6;
    // Create the arc generator.
    vis.arc = d3
      .arc()
      .startAngle((d) => d.x0)
      .endAngle((d) => d.x1)
      .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005))
      .padRadius(vis.radius * 1.5)
      .innerRadius((d) => d.y0 * vis.radius)
      .outerRadius((d) => Math.max(d.y0 * vis.radius, d.y1 * vis.radius - 1));
    // Create the SVG container.
    vis.svg = d3
      .select(vis.config.parentElement)
      .append("svg")
      .attr("viewBox", [-vis.width / 2, -vis.height / 2, vis.width, vis.width])
      .style("font", "10px sans-serif");

    vis.label = vis.svg
      .append("g")
      .attr("pointer-events", "none")
      .attr("text-anchor", "middle")
      .style("user-select", "none");
    vis.color = d3.scaleOrdinal(
      d3.quantize(d3.interpolateRainbow, vis.data.children.length + 1)
    );
  }

  /**
   * Prepare the data and scales before we render it.
   */
  updateVis() {
    let vis = this;
    vis.hierarchy = d3
      .hierarchy(vis.data)
      .sum((d) => d.value)
      .sort((a, b) => b.value - a.value);
    vis.root = d3.partition().size([2 * Math.PI, vis.hierarchy.height + 1])(
      vis.hierarchy
    );
    vis.root.each((d) => (d.current = d));

    vis.renderVis();
  }

  /**
   * Bind data to visual elements.
   */
  renderVis() {
    let vis = this;

    // Append the arcs.
    const path = vis.svg
      .append("g")
      .selectAll("path")
      .data(vis.root.descendants().slice(1))
      .join("path")
      .attr("fill", (d) => {
        while (d.depth > 1) d = d.parent;
        return vis.color(d.data.name);
      })
      .attr("fill-opacity", (d) => {
        return vis.arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0;
      })
      .attr("pointer-events", (d) =>
        vis.arcVisible(d.current) ? "auto" : "none"
      )
      .attr("d", (d) => vis.arc(d.current));
    console.log(path);
    // Make them clickable if they have children.
    path
      .filter((d) => d.children)
      .style("cursor", "pointer")
      .on("click", this.clicked);
    const format = d3.format(",d");
    path.append("title").text(
      (d) =>
        `${d
          .ancestors()
          .map((d) => d.data.name)
          .reverse()
          .join("/")}\n${format(d.value)}`
    );
    const labels = vis.label
      .selectAll("text")
      .data(vis.root.descendants().slice(1))
      .join("text")
      .attr("dy", "0.35em")
      .attr("fill-opacity", (d) => vis.labelVisible(d.current))
      .attr("transform", (d) => vis.labelTransform(d.current, vis.radius))
      .text((d) => d.data.name);
    const parent = vis.svg
      .append("circle")
      .datum(vis.root)
      .attr("r", vis.radius)
      .attr("fill", "none")
      .attr("pointer-events", "all")
      .on("click", this.clicked);
  }
  // Handle zoom on click.

  clicked(event, p) {
    parent.datum(p.parent || vis.root);

    vis.root.each(
      (d) =>
        (d.target = {
          x0:
            Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) *
            2 *
            Math.PI,
          x1:
            Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) *
            2 *
            Math.PI,
          y0: Math.max(0, d.y0 - p.depth),
          y1: Math.max(0, d.y1 - p.depth),
        })
    );

    const t = svg.transition().duration(750);

    // Transition the data on all arcs, even the ones that aren’t visible,
    // so that if this transition is interrupted, entering arcs will start
    // the next transition from the desired position.
    path
      .transition(t)
      .tween("data", (d) => {
        const i = d3.interpolate(d.current, d.target);
        return (t) => (d.current = i(t));
      })
      .filter(function (d) {
        return +this.getAttribute("fill-opacity") || vis.arcVisible(d.target);
      })
      .attr("fill-opacity", (d) =>
        vis.arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0
      )
      .attr("pointer-events", (d) =>
        vis.arcVisible(d.target) ? "auto" : "none"
      )

      .attrTween("d", (d) => () => arc(d.current));

    label
      .filter(function (d) {
        return +this.getAttribute("fill-opacity") || vis.labelVisible(d.target);
      })
      .transition(t)
      .attr("fill-opacity", (d) => +vis.labelVisible(d.target))
      .attrTween(
        "transform",
        (d) => () => vis.labelTransform(d.current, vis.radius)
      );
  }
  arcVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
  }

  labelVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
  }

  labelTransform(d, radius) {
    const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
    const y = ((d.y0 + d.y1) / 2) * radius;
    return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
  }
}