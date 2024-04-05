class directory {
  /**
   * Class constructor with basic chart configuration
   * @param {Object}
   * @param {Array}
   */
  constructor(
    _config,
    _data,
    _dispatcher,
    _currValue,
    _diff,
    _fileName,
    _state
  ) {
    this.config = {
      parentElement: _config.parentElement,
      containerWidth: _config.containerWidth || 800,
      containerHeight: _config.containerHeight || 1000,
      margin: _config.margin || { top: 25, right: 20, bottom: 20, left: 35 },
      tooltipPadding: _config.tooltipPadding || 15,
    };
    this.data = _data;
    this.dispatcher = _dispatcher;
    this.currValue = _currValue;
    this.diff = _diff;
    this.fileName = _fileName;
    this.state = _state;
    this.showDiff = false;
    this.initVis();
  }

  /**
   * We initialize and append static elements
   */
  initVis() {
    let vis = this;
    vis.width =
      vis.config.containerWidth -
      vis.config.margin.left -
      vis.config.margin.right;

    vis.height = vis.width;
    vis.radius = vis.width / 12;

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
      // .attr("viewBox", [-vis.width / 2, -vis.height / 2, vis.width, vis.width])
      .attr("viewBox", [-200, -200.5, 745, 745])
      .style("font", "8px sans-serif");

    vis.label = vis.svg
      .append("g")
      .attr("pointer-events", "none")
      .attr("text-anchor", "middle")
      .style("user-select", "none");

    vis.color = d3.scaleOrdinal(
      d3.quantize(d3.interpolateRainbow, vis.data.children.length + 1)
    );

    vis.min = 1;
    vis.max = vis.fileName.length;
    vis.slider = d3
      .sliderBottom()
      .min(vis.min)
      .max(vis.max)
      .step(1)
      .width(500)
      .ticks(vis.fileName.length - 1)
      .tickFormat(d3.format(",.0f"))
      .default(false)
      .on("onchange", (val) => {
        vis.dispatcher.call("timeline", event, val, vis.currValue);
      });

    vis.time = d3.select("#time-text");

    d3.select("div#slider")
      .append("svg")
      .attr("width", 550)
      .attr("height", 100)
      .append("g")
      .attr("transform", "translate(30,30)")
      .call(vis.slider);

    this.updateVis();
  }

  /**
   * Prepare the data and scales before we render it.
   */
  updateVis() {
    let vis = this;

    vis.hierarchy = d3
      .hierarchy(vis.data)
      .sum((d) => {
        return d.size;
      })
      .sort((a, b) => b.size - a.size);
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

    // text
    vis.time.join("p").text("Time stamp at " + vis.fileName[vis.state]);

    // Append the arcs.
    vis.path = vis.svg
      .join("g")
      .selectAll("path")
      .data(vis.root.descendants().slice(1))
      .join("path")
      .attr("fill", (d) => {
        if (vis.showDiff && vis.diff != undefined && vis.diff.includes(d.data.name)) {
          return "#F4CF20";
        } else {
          while (d.depth > 1) d = d.parent;
          return vis.color(d.data.name);
        }
      })
      .attr("fill-opacity", (d) => {
        return vis.arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0;
      })
      .attr("pointer-events", (d) =>
        vis.arcVisible(d.current) ? "auto" : "none"
      )
      .attr("d", (d) => vis.arc(d.current));

    // Make them clickable if they have children.
    vis.path
      .filter((d) => d.children)
      .style("cursor", "pointer")
      .on("click", (event, d) => {
        this.clicked(event, d, vis, labels);
      });

    const format = d3.format(",d");

    vis.path.join("title").text((d) => {
      return `${d
        .ancestors()
        .map((d) => d.data.name)
        .reverse()
        .join("/")}\n${format(d.value)}`;
    });

    let labels = vis.label
      .selectAll("text")
      .data(vis.root.descendants().slice(1))
      .join("text")
      .attr("dy", "0.25em")
      .attr("font-weight", (d) => {
        if (vis.diff != undefined && vis.diff.includes(d.data.name)) {
          return "900";
        } else {
          return "400";
        }
      })
      .attr("fill-opacity", (d) => {
        return vis.labelVisible(d.current);
      })
      .attr("transform", (d) => vis.labelTransform(d.current, vis.radius))
      .text((d) => d.data.name);

    vis.parent = vis.svg
      .append("circle")
      .datum(vis.root)
      .attr("r", vis.radius)
      .attr("fill", "none")
      .attr("pointer-events", "all")
      .on("click", (event, d) => {
        this.clicked(event, d, vis, labels);
      });
  }
  // Handle zoom on click.

  clicked(event, p, vis, label) {
    vis.parent.datum(p.parent || vis.root);

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

    const t = vis.svg.transition().duration(750);

    // Transition the data on all arcs, even the ones that aren’t visible,
    // so that if this transition is interrupted, entering arcs will start
    // the next transition from the desired position.
    vis.path
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

      .attrTween("d", (d) => () => vis.arc(d.current));

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
    if (d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03) {
      return 1;
    } else {
      return 0;
    }
  }

  labelTransform(d, radius) {
    const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
    const y = ((d.y0 + d.y1) / 2) * radius;
    return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
  }
}
