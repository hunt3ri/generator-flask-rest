'use strict';
var yeoman = require('yeoman-generator');
var chalk = require('chalk');
var yosay = require('yosay');
var mkdirp = require('mkdirp');

module.exports = yeoman.generators.Base.extend({
    prompting: function () {
        var done = this.async();

        // Have Yeoman greet the user.
        this.log(yosay(
            'Welcome to the spectacular ' + chalk.red('generator-flask-rest') + ' generator!'
        ));

        var prompts = [{
            type: 'input',
            name: 'appName',
            message: "What's the name of your app: ",
            default: function () {
                return 'Flask-Rest'
            }
        }];

        this.prompt(prompts, function (props) {
            this.appName = props.appName;
            // To access props later use this.props.someOption;

            done();
        }.bind(this));
    },

    writing: {
        app: function () {
            console.log('Scaffolding Flask Basic app in directory : ' + this.appName);
            mkdirp(this.appName);
            
            // Copy root dir files individually, can't use bulk copy here
            this.copy('_root/__init__.py', appDir + '/__init__.py', null);
            this.copy('_root/manage.py', this.appName + '/manage.py', null);
            this.copy('_root/.gitignore', this.appName + '/.gitignore', null);
            
            // Copy scaffold files into the app
            var appDir = this.appName + "/app";
        }
    },
    
    install: function () {
      console.log("One more thing.  Creating python virtual environment...");
      this.spawnCommand('pyvenv', [this.appName + '/venv']);
      /*this.spawnCommand('source', ['./' + this.appName + '/venv/bin/activate']);*/
  }
});
