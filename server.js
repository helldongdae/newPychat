// Server code
// To execute, simply type node server.js in the terminal
var net = require('net');
var users = [];
var chatrooms = [];
var connected = 0;

var svr = net.createServer(function(sock) {
    console.log('Connected: ' + sock.remoteAddress + ':' + sock.remotePort);
    var usrName = ''
    sock.on('data', function(chunk) {
	var toText = chunk.toString('utf8');
	var operands = toText.split(' ');
	if(operands[0] == 'USERNAME'){
		var q = true;
		for(i = 0;i<users.length;i++){
			if(users[i].name == operands[1])
				q = false;
		}
		if(!q)
			sock.write("FAIL");
		else{
			usrName = operands[1];
			users.push({name:operands[1], socket:sock});
			sock.write("SUCCESS")
		}
	}
	
	else if(operands[0] == 'NEW_ROOM'){
		var q = true;
		console.log(operands[1])
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].name == operands[1])
				q = false;
		}
		if(!q)
			sock.write("FAIL");
		else{
			var init_mem = [];
			init_mem.push(usrName)
			chatrooms.push({name:operands[1], member:init_mem});
			sock.write("SUCCESS")
		}
	}

	else if(operands[0] == 'REFRESH'){
		var q = "";
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].member.indexOf(usrName) != -1)
				q += chatrooms[i].name + " ";
		}
		if(q.length == 0)
			q = " ";
		sock.write(q);
	}

	else if(operands[0] == 'SEND_ME_EXIT_CODE'){
		sock.write('exit()');
	}
    });

    // End of connection. delete all of the created sockets and exit
    sock.on('end', function() {
	console.log("Connetion Lost");
	var q = users.indexOf(usrName);
	users.splice(q, 1);
    });
    
});

var svraddr = '127.0.0.1';
var svrport = 8080;
 
svr.listen(svrport, svraddr);
console.log('Server Created at ' + svraddr + ':' + svrport + '\n');
