const path = require('path');
const nodeExternals = require('webpack-node-externals');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

const lambdaConfig = {
  target: 'node',
  entry: './frontend/lambda/lambda.ts',
  // Tried source-map-support but the line numbers are weird, so
  // disabling source map support for now.
  devtool: undefined,
  mode: 'development',
  externals: [nodeExternals()],
  output: {
    filename: 'lambda.js',
    path: path.resolve(__dirname)
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        exclude: /node_modules/,
        use: [
          { loader: 'ts-loader' }
        ]
      }
    ]
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.js' ]
  },

};

const webConfig = {
  target: 'web',
  entry: ['babel-polyfill', './frontend/lib/main.ts'],
  devtool: 'inline-source-map',
  mode: 'development',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'frontend', 'static', 'frontend')
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        exclude: /node_modules/,
        use: [
          { loader: 'babel-loader' },
          { loader: 'ts-loader' }
        ]
      }
    ]
  },
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
    })
  ],
  resolve: {
    extensions: [ '.tsx', '.ts', '.js' ]
  },
};

module.exports = [ lambdaConfig, webConfig ];
