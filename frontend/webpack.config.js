const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname,'./static/frontend'),
    filename:"[name].js",

  },
   devServer: {
    historyApiFallback: true,
    contentBase: './',
    hot: true
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)?$/,
        exclude: /node_modules/,
        use: {
            loader: "babel-loader",
            options: { presets: ["@babel/env"] }

        },
    },
    {
        test: /\.(png|jpe?g|gif|ico|svg)$/i,
        use: [
            {
                loader: 'file-loader',
            },
        ],
    },
    {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
    },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV' :JSON.stringify("development"),
    })
  ],
  resolve: {
    extensions: [".js",".jsx"],
}
};