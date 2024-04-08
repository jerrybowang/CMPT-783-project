class port {
  /**
   * Class constructor with basic chart configuration
   * @param {Object}
   * @param {Array}
   */
  constructor(_config, _data, _dispatcher, _currValue, _diff) {
    this.config = {
      parentElement: _config.parentElement,
      containerWidth: _config.containerWidth,
      containerHeight: _config.containerHeight,
      margin: _config.margin || { top: 25, right: 20, bottom: 20, left: 35 },
      tooltipPadding: _config.tooltipPadding || 15,
    };
    this.data = _data;
    this.dispatcher = _dispatcher;
    this.currValue = _currValue;
    this.diff = _diff;
    this.showDiff = false;
    this.initVis();
  }

  /**
   * We initialize scales/axes and append static elements, such as axis titles.
   */
  initVis() {
    let vis = this;

    vis.container = d3
      .select(vis.config.parentElement)
      .attr("position", "relative")
      .attr("padding", "70px");

    vis.table = vis.container
      .append("table")
      .attr("class", "table")
      .style("border-collapse", "collapse")
      .style("border", "2px black solid");
    vis.thead = vis.table.append("thead");
    vis.tbody = vis.table.append("tbody");
    this.updateVis();
  }

  /**
   * Prepare the data and scales before we render it.
   */
  updateVis() {
    let vis = this;
    vis.data.openPorts = vis.data.openPorts.sort((a, b) => a.port - b.port);

    vis.renderVis();
  }

  /**
   * Bind data to visual elements.
   */
  renderVis() {
    let vis = this;

    vis.thead
      .join("tr")
      .selectAll("th")
      .data(["Port Information"])
      .join("th")
      .text((d) => d)
      .style("border", "1px black solid")
      .style("padding", "5px")
      .style("background-color", "lightgray")
      .style("font-weight", "bold")
      .style("text-transform", "uppercase");

    vis.rows = vis.tbody
      .selectAll("tr")
      .data(() => {
        return vis.data.openPorts;
      })
      .join("tr");

    vis.cells = vis.rows
      .selectAll("td")
      .data((d) => [d])
      .join("td")
      .text((d) => ["Ports: " + d.port + "  Name:  " + d.name])
      .style("border", "1px black solid")
      .style("padding", "5px")
      .style("background", (d) => {
        if (
          vis.showDiff &&
          vis.diff != undefined &&
          vis.diff.includes(d.port)
        ) {
          return "#F4CF20";
        }
      });
  }
}
