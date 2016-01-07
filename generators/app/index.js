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
            this.copy('_root/manage.py', this.appName + '/manage.py', null);
            this.copy('_root/.gitignore', this.appName + '/.gitignore', null);
            this.copy('_root/requirements.txt', this.appName + '/requirements.txt', null);
            
            // Copy scaffold files into the app
            this.bulkDirectory('_app', this.appName + "/app", null)
            this.bulkDirectory('_templates', this.appName + "/templates", null)
            this.bulkDirectory('_web', this.appName + "/web", null)
        }
    },
    
    install: function () {
      console.log("Creating python virtual environment...");
      this.spawnCommandSync('pyvenv', [this.appName + '/venv']);
      
      
      
  }
});
