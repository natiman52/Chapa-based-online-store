const path = require("path")
const webpack = require("webpack")
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
module.exports = {
    entry:"./assets/index.js",
    output:{
        filename:"bundle.js",
        path:path.resolve(__dirname,"staticfiles")
    },
    module:{
        rules:[
            {
                test:/\.(sa|sc|c)ss$/,
                use:[MiniCssExtractPlugin.loader,"css-loader","sass-loader"],
                sideEffects: true,
            },
            
        ]
    },
    plugins:[new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery' 
      }),new MiniCssExtractPlugin({filename:'[test].css'})]
}