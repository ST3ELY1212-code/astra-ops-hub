const { health } = require("../control/loop");
module.exports = async function handler(_req, res) {
  res.status(200).json(health());
};
