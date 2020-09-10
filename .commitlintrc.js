module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
      'header-max-length': [2, 'always', 72],
      'type-empty': [2, 'never'],
      'type-enum': [2, 'always', [
        "feat", "fix", "docs", "style", "refactor", "test", "perf", "ci", "chore", "build", "revert"
      ]],
  }
};