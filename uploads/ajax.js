ajax = ajax.createModule(function() {
	var xmlHttpRequest = function() {
		var xmlHttp = null;
		try {
			xmlHttp = new XMLHttpRequest();
		} catch (e) {
			try {
				xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
		}
		return xmlHttp;
	}
	var function_ajax_callback = function(callback, response, div) {
		dump.next('entro nella funzione callback');
		var json_obj = eval("(" + response + ")");
		if (typeof(json_obj) == 'object') {
			return callback(json_obj, div);
		}
	}
	var ajaX = function(method, url, div, callback, data) {
		var httpRequest = xmlHttpRequest();
		var handler = function() {
			var response = httpRequest.responseText;
			if (httpRequest.readyState == 4) {
				if (httpRequest.status == 200) {
					//if(!document.getElementById(div)) var div = document.getElementById('main');
					//var target = document.getElementById(div);
					try {
						dump.next('provo a eseguire callback');
						function_ajax_callback(callback, response, div);
						dump.next('ajax obj ok');
					} catch (e) {
						dom.do_alert('info', response);
						//target.innerHTML = response;
						dump.next('ajax txt ok');				
					}
				}
			}
		}
		httpRequest.onreadystatechange = handler;
		httpRequest.open(method, url, true);
		if (method == "get") {
			httpRequest.send(null);
		}
		if (method == "post") {
			httpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=iso-8859-1");
			httpRequest.send(data);
			dump.next('ajax post ok');
		}
	}
	var ajaxGet = function(url, div, callback) {
		return ajaX('get', url, div, callback);
	}
	var ajaxPost = function(url, div, callback, data) {
		return ajaX('post', url, div, callback, data);
	}
	return {
		function_ajaxGet: ajaxGet,
		function_ajaxPost: ajaxPost
	}
});