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
            var appDir = this.appName + "/app";

            this.fs.copyTpl(
                this.templatePath('_root/package.json'),
                this.destinationPath(this.appName + '/package.json'),
                {name: this.appName}
            );


        }
    },

    install: function () {
        var npmdir = process.cwd() + this.appName;
        process.chdir(npmdir);

        this.installDependencies()
    }
});
