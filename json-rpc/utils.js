const fs = require('fs');

module.exports = {
  sum({ a, b }) {
    return a + b;
  },
  createFile({ filename, content }) {
    try {
      fs.writeFileSync(filename, content);
      return true;
    } catch {
      return false;
    }
  },
  initialize(params) {
    console.log(params);
  }
};
