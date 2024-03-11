let dir, dataset;
d3.json("data/onlineData.json").then((data) => {
  dataset = data;
  dir = new directory(
    {
      parentElement: "#directory-container",
    },
    data
  );
  dir.updateVis();
});
