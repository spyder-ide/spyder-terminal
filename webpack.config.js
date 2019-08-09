const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = { 
  entry: path.join(__dirname, 'spyder_terminal', 'server', 'static', 'js', 'main.js'), 
  output: {    
    path: path.join(__dirname, 'spyder_terminal', 'server', 'static', 'build'),
    filename: 'main.bundle.js'
  },
  mode: 'development',
  resolve: {
    modules: ['node_modules']
  },
  devServer: {
    contentBase: path.join(__dirname, 'spyder_terminal', 'server', 'static')
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, 'spyder_terminal', 'server', 'static', 'index.html')
    })
  ]
};
