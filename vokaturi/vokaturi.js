var PythonShell = require('python-shell');

module.exports = function(RED) {

  function VokaturiOptions(config) {
    RED.nodes.createNode(this,config);

  }

  //RED.nodes.registerType('vokaturi-options', VokaturiOptions);


  function VokaturiNode(config) {
    RED.nodes.createNode(this,config);
    var node = this;
    this.options = RED.nodes.getNode(config.options);
    node.on('input', function(msg) {

      var options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: __dirname + '/python/',
        args: [msg.payload]
      };

      PythonShell.run('vokaturi.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution



        //take the last element of results (JSON) and set the payload

        var result = JSON.parse(results[results.length -1]);

        if(result.valid !== 1){
                console.log('results: %j', results);
        }

        msg.payload = result;


        //send msg
        node.send([msg]);
      });



    });
  }
  RED.nodes.registerType("vokaturi",VokaturiNode);
}
