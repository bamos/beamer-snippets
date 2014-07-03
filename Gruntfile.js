module.exports = function(grunt) {
  grunt.initConfig({

    // Various Grunt tasks...

    buildcontrol: {
      options: {
        dir: 'dist',
        commit: true,
        push: true,
        message: 'Built %sourceName% from commit %sourceCommit% on branch %sourceBranch%.'
      },
      pages: {
        options: {
          remote: 'git@github.com:bamos/beamer-snippets.git',
          branch: 'gh-pages'
        }
      }
    }
  });
  grunt.loadNpmTasks('grunt-build-control');
  grunt.registerTask('deploy', ['buildcontrol:pages']);
}
