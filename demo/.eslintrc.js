module.exports = {
    parserOptions: {
        parser: 'babel-eslint',
        ecmaVersion: 2020,
        allowImportExportEverywhere: true
    },
   overrides: [
       {
           files: ['src/views/**/*.vue'],
           rules: {
               'vue/multi-word-component-names': 0,
      },
    },
  ],
}