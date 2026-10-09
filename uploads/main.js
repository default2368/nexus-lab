/*
$(document).ready(function(){
	$("#lead").html("This is Hello World by JQuery");
});*/

main = main.extend(function(){
  	
	dump.next('init');
	if(sessionStorage.getItem('req')){
		sessionStorage.removeItem('req');			
	}
	
	/* app vars obj, array, ecc */
	
	var a1 = ['id_game','select_game']; //1 - seleziona partita
	var a2 = ['ally_is_set','select_ally']; //2 - seleziona alleanza
	var a3 = ['tables_exists','do_game_tables']; //3 - imposta tabelle
	var arraySupremacy = new Array(a1,a2,a3);
	
	var objCallback = {
		'alliance': supr.list_alliance,
		'do_table' : dom.main_table,
		'view_record' : dom.view_record,
		'edit_record' : dom.edit_record,
		'new_record' : dom.new_record,
		'do_select': dom.build_select,
		'select_game' : supr.select_game,
		'do_init_controls' : supr.do_init_controls,
		'select_ally' : supr.select_ally,
		'do_game_tables' : supr.do_game_tables,
		'get_response' : dom.test_obj,
		'truncate_tables' : dom.truncate_tables
	};
	
	/* new functions */
	
	var setObjUrls = function(array){//array formato dalle n coppie name=value
		return main.map(array, getQueryStr);		
	}
	
	/*
	var staticAjax = function(){
		var y = main.new_url_array('id_game', localStorage.getItem('id_game'), 'do_game_tables');
		main.do_ajax('do_game_tables', y);
	}
	*/
	
	var doAjaxAll = function(a){// array object storage
		dump.next('test initAjax');
		setObjUrls(a);
		dom.dom_control();
		return main.map(getArrayStorage(), doAjax);
		/* 
		esegue tutte le istanze presenti nell'array object passando 
		come argomento alla funzione doAjax l'action 
		*/
	}
	
	var newUrlArray = function(name, value, action){
		//var y = main.new_url_array('id_game', localStorage.getItem('id_game'), 'do_game_tables');
		var x, my_url;
		if(arguments[2]){
			x = action;
			my_url = '?action=' + x;
		} else {
			main.get_obj_storage();
			x = getArrayStorage();
			my_url = '?action=' + x[0];
		}
		if(arguments[3]){
			userObj.sections[action].url = my_url;
		}
		my_url += '&' + name + '=' + value;
		return new Array(my_url);
	}
	
	var launchAjax = function(action, storage){
		var x, name, value, my_url;
		x = action;
		my_url = '?action=' + x;
		if(arguments[1]){
			name = storage;
			value = localStorage.getItem(storage);
			my_url += '&' + name + '=' + value;	
		} 		
		//dump.next('test nuovo indirizzo' + my_url);
		return doAjax(action, my_url);
	}
	
	/* -------------------------------------*/
	
	var getQueryStr = function(a) {
		/*
		prende come argomento 1 array nella forma name=value, analizza elemento, 
		se presente nelle istanze lo inserisce nell'array storage, va a completare
		l'array url dell'oggetto iniziale userObj
		*/		
		var b = userObj.cfg;
		var e = a.split("=");
		var x = e[0];
		var y = e[1];
		if (main.in_array(x, b.instances)) {
			if (sessionStorage.getItem('url')) {
				sessionStorage.removeItem('url');
			}
			sessionStorage.setItem('url', '?' + x + '=' + y);
			main.get_obj_storage();			
			addToArrayStorage(y);			
			try {
				myArray = userObj.sections[y].url;
				myArray.push(sessionStorage.getItem('url'));
			} catch (e) {
				dom.do_msg('lead', 'Si e verificato un errore');
			}
		} else {
			if(x === 't' ) sessionStorage.setItem('active-table', y);
			try {
				sessionStorage.setItem('url', sessionStorage.getItem('url') + '&' + x + '=' + y);
				myArray.pop();
				myArray.push(sessionStorage.getItem('url'));				
			} catch (e) {
				dom.do_msg('lead', 'Si e verificato un errore indefinito');
			}
		}		
	}
	
	var doAjax = function(i){			
		var b = userObj.sections;		
		switch(i){			
			default:
				var my_url;
				if(arguments[1]){
					my_url = b[i].server_url + arguments[1];
				} else {
					if(b[i].server_url){
						my_url = b[i].server_url + b[i].url;						
					} else {
						my_url = userObj.cfg.server_url + b[i].url;
					}
				}
				var my_callback = objCallback[i];
				var my_div = b[i].div;
				if(!b[i].post){
					dump.next('eseguo ajax');
					ajax.function_ajaxGet(my_url, my_div, my_callback);										
				}else{
					ajax.function_ajaxPost(my_url, userObj.cfg.div_main, null, sessionStorage.getItem('form_data'));
					if(userObj.cfg.redirect_on_post == 'y'){
						setTimeout(function(){ window.location.href=userObj.cfg.index_file; }, 2500);
					}
				}				
			break;
		}			
	}
	
	var init_app = function(){
		main.get_obj_storage();
		reseArrayStorage();
		var a = location.search.substr(1);
		var array_query_string  = a.split("&");
		if(!a) {
			//var my_string_url = new Array('sub=do_select','t=t_nazioni', 'action=do_table', 't=t_nazioni');
			//var my_string_url = new Array('action=wizard_game');			
			//supr.my_test();
			supr.app_supremacy();
		} else {
			if(a && a.indexOf("&") == -1 || a.indexOf("&") !== -1){
				//setObjUrls(b);
				doAjaxAll(array_query_string);
				/*
				var b = userObj.sections;
				dump.next('Controllo oggetto userObj');
				dump.inspect(b.do_table);
				dump.inspect(b.do_select);
				*/
			}           
		}		
	};
	
	
	return {
		init: init_app, 
		set_obj_urls: setObjUrls, 
		do_ajax_all: doAjaxAll,			
		get_query_str: getQueryStr, 
		do_ajax: doAjax,
		launch_ajax: launchAjax,
		//my_app_function: myAppFunction,		
		array_supremacy: arraySupremacy,
		new_url_array: newUrlArray
	}
		/*get_query_string: getQueryStr, get_obj_storage: getObjStorage, get_values_do_ajax: getValuesDoAjax, set_obj_storage: setObjStorage }*/
});

(function(){	
	main.init();	
	//main.do_request();	
})();

/*
var myAppFunction_copia2 = function(my_array){//supremacy_array		
		var setUrlGetStorage = function(my_array){ //splitProcedureArray
			var my_string_url;
			var x = my_array[0];
			var y = my_array[1];
			my_string_url = new Array('action=' + y);
			//setObjUrls(buildUrlArray(y));
			setObjUrls(my_string_url);//main.map(my_string_url, main.url_engine);
		}
		main.map(my_array, setUrlGetStorage);//work on supremacy array
		/* start my app 
		main.get_obj_storage();
		var arrayObj = getArrayStorage();
		myAppElement = function(){			
			var my_key = my_array[0][0];
			if(localStorage.getItem(my_key)){ 
				my_array.shift();
				arrayObj.shift();
				setArrStorage(arrayObj);				
			} else {
				var x = (arguments[0], localStorage.getItem(arguments[0]), 'select_ally');
				main.do_ajax('select_ally', x);				
				var array_obj_storage = arrayObj;				
				doAjax(array_obj_storage[0]);				
			}			
		}
	}

	var myAppFunction_copia1 = function(my_array){//supremacy_array		
		var setUrlGetStorage = function(my_array){ //splitProcedureArray
			var x = my_array[0];
			var y = my_array[1];
			var my_string_url = new Array('action=' + y);
			//setObjUrls(buildUrlArray(y));
			setObjUrls(my_string_url);//main.map(my_string_url, main.url_engine);
		}
		main.map(my_array, setUrlGetStorage);//work on supremacy array
		/* start my app *
		main.get_obj_storage();
		var arrayObj = getArrayStorage();
		myAppElement = function(){			
			var my_key = my_array[0][0];
			if(localStorage.getItem(my_key)){ 
				my_array.shift();
				arrayObj.shift();
				setArrStorage(arrayObj);
				/* debug 
				dump.next('obj storage se localstorage trovato');
				dump.inspect(arrayObj);
				
			} else {
				/* debug
				dump.next('obj storage se localstorage non trovato');
				dump.inspect(arrayObj);
				
				var array_obj_storage = arrayObj;				
				doAjax(array_obj_storage[0]);				
			}			
			/* debug
			dump.next('lunghezza array storage :' + returnArrayLength());
			
		}
	}

var esegui_richiesta_IS_OLD = function(){			
	var an_array = [];
	var key_localstorage = my_procedure_array[0][0];
	if(localStorage.getItem(key_localstorage)){
		my_procedure_array.shift();				
	} else {
		dump.next('localstorage non esistente');				
		main.single_request(arrayReq[0]);
		
		
		an_array.push(arrayReq[0]);
		sessionStorage.setItem("req", JSON.stringify(an_array));
		main.do_request();
		
	}
	arrayReq.shift();
	sessionStorage.setItem('req', JSON.stringify(arrayReq));
}

var doRequest_IS_OLD = function(){
	var arrayReq = JSON.parse(sessionStorage.getItem("req"));
	/* tutta questa parte è inutile 
	if(arrayReq) {
		var keys = Object.keys(arrayReq);
		if(keys.length > 1){
		dom.dom_control();
				dump.next('richieste maggiori di 1');
		}
		dump.next('numero richieste ' + keys.length);			
		dom.dom_control();
		//test('my_test');
	}
	/* fine parte inutile 
	main.map(arrayReq, myRequest);			
	//dump.next('esco dalla funzione do_request')
}

var myAppFunction_COPIA = function(my_array){//supremacy_array		
	var f = function(my_array){ //splitProcedureArray
		var x = my_array[0];
		var y = my_array[1];
		var my_string_url = new Array('action=' + y);
		//setObjUrls(buildUrlArray(y));
		setObjUrls(my_string_url);//main.map(my_string_url, main.url_engine);
	}
	main.map(my_array, f);//work on supremacy array
	main.get_obj_storage();
	var array0 = getArrayStorage();
	myAppElement = function(){			
		var my_key = my_array[0][0];
		if(localStorage.getItem(my_key)){ 
			my_array.shift();
		} else {
			var array_obj_storage = array0;				
			doAjax(array_obj_storage[0]);				
		}			
		array0.shift();			
		setArrStorage(array0);
	}
}
*/
