// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:5000/'
      }
    }
  },
  chainWebpack: config => {
    config.module
      .rule('yaml-loader')
      .test(/\.ya?ml$/)
      // .type('json')
      .use('js-yaml-loader')
      .loader('js-yaml-loader')
      .end()
  },
  configureWebpack: {
    optimization: {
      minimize: true,
      splitChunks: {
        minSize: 100000,
        maxSize: 1000000,
        maxAsyncRequests: 6,
        maxInitialRequests: 4,
        chunks: 'all'
      }
    },
    entry: {
      index: './src/main.js',
      start: './src/views/Start.vue',
      wiser: './src/views/Wiser.vue',
      voting: './src/views/Voting.vue',
      complete: './src/views/Complete.vue',
      finish: './src/views/Finish.vue'
    }
  }
}
