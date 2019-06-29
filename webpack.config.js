const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


module.exports = {
  entry: "./src/index.jsx",
  output: {
    filename: 'bundle.js',
    path: __dirname + "/dist",
    publicPath: '/'
  },
  resolve: {
    extensions: [".jsx", ".js", ".json"]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html'
    }),
    new CleanWebpackPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      }
    ]
  },
};

// module.exports = {
//   entry: './src/index.jsx',
//   output: {
//     path: path.resolve(__dirname, 'dist'),
//     filename: 'bundle.js'
//   },
//   plugins: [
//     new HtmlWebpackPlugin({ template: './src/index.html' }),
//   ],
//   rules: [
//     {
//       test: /\.jsx?$/,
//       exclude: /node_modules/,
//       use: 'babel-loader',
//     }
//   ]
// };