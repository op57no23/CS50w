document.addEventListener('DOMContentLoaded', () => {

		var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

		socket.on('connect', () => {
				document.querySelector('#create_channel').onclick = () => {
						const channel_name = document.querySelector('#channel_name').value;
						var channel_input = document.querySelector("#channel_name");
						if (channel_input.checkValidity() === false){
								document.querySelector("#channel_name").value = "";
								return true;
						}
						document.querySelector("#channel_name").value = "";
						socket.emit('create_new_channel', {'channel_name': channel_name});
						return false;
				};

				document.querySelector('#send_message').onsubmit = () => {
						const message = document.querySelector('#message_input').value;
						document.querySelector("#message_input").value = "";
						const time = new Date().toLocaleTimeString();
						const channel_name  = document.querySelector(".list-group-item.list-group-item-action.active").id; 
						socket.emit('create_new_message', {'message': message, 'time': time, 'channel_name': channel_name});
						return false;
				};
		});

		socket.on('new message', data => {
				var message = document.createElement("div");
				message.setAttribute('class', 'row');
				if (data.user == document.querySelector("#username").innerHTML) {
						message.innerHTML = "<div class='col-6'></div><div class='col-6'><small>" + data.user + " at " + data.time + "</small><br>" + data.message + "</div>";
				}
				else {
						message.innerHTML = "<div class='col-6'><small>" + data.user + " at " + data.time + "</small><br>" + data.message + "</div><div class='col-6'></div>";

				}
				var parentNode = document.querySelector("#" + data.channel_name + "messages");
				parentNode.appendChild(message);
				parentNode.scrollTop = parentNode.scrollHeight;
		});

		socket.on('new channel', channel => {
				var listItem = document.createElement('button');
				listItem.setAttribute('class','list-group-item list-group-item-action');
				listItem.setAttribute('type', 'button');
				listItem.textContent = channel.channel_name;
				listItem.setAttribute('id', channel.channel_name);
				var parentNode = document.getElementById("listgroup");
				parentNode.insertBefore(listItem, document.getElementById("add_new_channel"));

				var div = document.createElement('div');
				div.setAttribute('class', 'col-10');
				div.setAttribute('style', 'display: none; height: 100%; overflow-y: scroll');
				div.setAttribute('id', channel.channel_name + "messages");
				var parentNode = document.querySelector("#messageWindow");
				parentNode.append(div);
		});

});


document.addEventListener('click', function(e) {
		if (e.target.tagName == "BUTTON" && (e.target.id != "add_new_channel" && e.target.className == "list-group-item list-group-item-action")) {
				document.querySelectorAll(".col-2 > .list-group > .list-group-item.list-group-item-action").forEach(function(el) {
						if (el.className == "list-group-item list-group-item-action active"){
								el.className = "list-group-item list-group-item-action";
						};
				});
				e.target.className = "list-group-item list-group-item-action active";
				document.querySelectorAll(".col-10[id]").forEach(function(el) { 
						el.style.display = "none";
				});
				var node = document.querySelector("#" + e.target.id + 'messages');
				node.style.display = "inline";
				node.scrollTop = node.scrollHeight;
				document.querySelector("#messageFormInput").style = "display: inline";
		}
});

