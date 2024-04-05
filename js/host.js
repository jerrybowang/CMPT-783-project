class host {
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
    vis.data.hosts = vis.data.hosts.sort((a, b) => a - b);

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
      .data(["Host IP Address"])
      .join("th")
      .text((d) => d)
      .style("border", "1px black solid")
      .style("padding", "5px")
      .style("background-color", "lightgray")
      .style("font-weight", "bold")
      .style("text-transform", "uppercase");

    vis.rows = vis.tbody.selectAll("tr").data(vis.data.hosts).join("tr");
    vis.cells = vis.rows
      .selectAll("td")
      .data((d) => [d])
      .join("td")
      .text((d) => d)
      .style("border", "1px black solid")
      .style("padding", "5px")
      .style("background", (d) => {
        if (vis.showDiff&&vis.diff != undefined && vis.diff.includes(d)) return "#F4CF20";
      });

  }
}
