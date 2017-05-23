// Server code
// To execute, simply type node server.js in the terminal
var net = require('net');
var users = [];
var chatrooms = [];
var propmes = [];
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
			init_mem.push(usrName);
			chatrooms.push({name:operands[1], member:init_mem, active:[]});
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

	else if(operands[0] == 'IN'){
		var roomN = operands[1];
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].name == roomN){
				chatrooms[i].active.push(usrName);
			}
		}
		for(i = 0;i<propmes.length;i++){
			if(propmes[i].rooms.indexOf(roomN) != -1){
				propmes[i].readUser.add(usrName);
				console.log(propmes[i].totalUser.size - propmes[i].readUser.size+' Users have not read')
			}
		}	
	}

	else if(operands[0] == 'OUT'){
		var roomN = operands[1];
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].name == roomN){
				var q = chatrooms[i].member.indexOf(usrName);
				chatrooms[i].active.splice(q, 1);
			}
		}	
	}

	else if(operands[0] == 'ADD_USER'){
		var usrN = operands[2];
		var roomN = operands[1];
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].name == roomN){
				if(chatrooms[i].member.indexOf(usrN) == -1){
					chatrooms[i].member.push(usrN);
					sock.write('SUCCESS');
				}
				else
					sock.write('FAIL');
			}
		}	
	}

	else if(operands[0] == 'GET_USER'){
		var usrs = '';
		for(i = 0;i<users.length;i++){
			usrs += users[i].name + ' ';
		}	
		sock.write(usrs);
	}

	else if(operands[0] == 'SEND_ME_EXIT_CODE'){
		sock.write('exit()');
	}

	else if(operands[0] == 'PROP'){
		var N = parseInt(operands[1]);
		var readed = 0;
		var readUser = new Set();
		var totalUser = new Set();
		var proped = {rooms:[], start:usrName, left:0, readUser:new Set(), totalUser:new Set()};	
		for(i = 2;i<N+2;i++){
			proped.rooms.push(operands[i])
			for(j = 0;j<chatrooms.length;j++){
				if(chatrooms[j].name == operands[i]){
					for(k = 0;k<chatrooms[j].member.length;k++){
						totalUser.add(chatrooms[j].member[k]);
					}
					for(k = 0;k<chatrooms[j].active.length;k++){
						readUser.add(chatrooms[j].active[k]);
					}
				}
			}
		}
		proped.left = totalUser.size - readUser.size;
		proped.readUser = readUser;
		proped.totalUser = totalUser;
		console.log(proped.left+' People have not read this')
		propmes.push(proped);
	}

	else if(operands[0] == 'CHAT'){
		var roomN = operands[1];
		var msg = ''
		for(i = 2;i<operands.length;i++){
			msg += operands[i] + ' ';
		}
		for(i = 0;i<chatrooms.length;i++){
			if(chatrooms[i].name == roomN){
				for(j = 0;j<chatrooms[i].active.length;j++){
					if(chatrooms[i].active[j] != usrName){
						var na = chatrooms[i].active[j];
						for(k = 0;k<users.length;k++){
							if(users[k].name == na)
								users[k].socket.write(msg);
						}
					}
				}
			}
		}			
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
