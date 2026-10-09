supr = supr.createModule(function(){
	
	var doAuth = function(){
		var my_form = document.f_login;
		var my_md5 = hex_md5(hex_md5(my_form.password.value));
		document.f_login.password.value = my_md5;
		my_form.submit();		
	}
	
	/* callbacks */
	
	/*
	var testObj = function(object, target, action){
		dom.do_msg('heading', 'Test nuova funzione');
		//var my_obj = object['table'];
		if(object.status === 1){
			doAlert('info', object.msg);//'selezione partita');						
		} else  {
			doAlert('alert', object.msg);			
		}	
	}
	*/
	
	var listAlliance = function(object,target){
		dom.simple_list(object, 'panel', 'nazione', 'ul', 'li');	
	}
	
	var selectGame = function(object, target){
		dom.do_msg('heading', 'Impostazione Partita');
		dom.dom_control('ignore-obj_storage');			
		setOneCol('build-row');
		var my_obj = object['table'];
		if(object.status === 1){
			dom.do_msg('lead', object.msg);//'selezione partita');
			dom.build_select(my_obj, target, 'my_select','id_partita','commento','seleziona partita');
			listeners.new_listener('my_select','change', listeners.selected_option);			
		} else  {
			dom.do_alert('alert', object.msg, 'index.php?action=new_record&t=partite');			
		}		
	}
	var selectAlly_new = function(object, target){
		dom.do_msg('heading', 'Test, Controllo alleanza');
		dump.inspect(main.new_url_array('id_game',localStorage.getItem('id_game'), 'get_response'));
		dom.do_msg('lead', object.msg);
		dom.dom_control();
	}
	
	var selectAlly = function(object, target){
		main.new_url_array('id_game', localStorage.getItem('id_game'),'select_ally',true);
		dom.do_msg('heading', 'Impostazione Alleanza');
		dump.next('debug new url');
		dump.inspect(userObj.sections['select_ally'].url);
		dump.next(userObj.sections['select_ally'].url);		
		if(localStorage.getItem('ally_is_set') === 'n' || !localStorage.getItem('ally_is_set') ){
			dump.next('alleanza non impostata');
			if(object.status === 2){
				dom.do_msg('lead', object.msg);
				dom.dom_control();
				setOneCol('build-row');
				var my_obj = object.table;
				dom.simple_list(my_obj, 'main', 'nazione', 'ul', 'li');//here!!!
				dom.new_button(3, 'main','b_select', 'Popola Tabelle', null);
				localStorage.setItem('ally_is_set','y');
			} else if(object.status === 1){
				var my_obj = object['table'];
				dom.do_msg('lead', object.msg);
				dom.dom_control();
				setForm();
				setTwoCols(6, 'my_form');
				dom.build_select(my_obj, 'main', 'my_select','id','nazione');
				var my_options = document.getElementById('my_select');
				my_options.multiple = true;
				my_options.size = 10;			
				dom.new_button(0, 'main','b_select', 'Scegli Nazione', null);//listeners.test_listener);
				//listeners.test_listener('my_select','click');
				var btn = document.getElementById('b_select');
				btn.addEventListener('click', listeners.select_multiple);
				btn.onclick = function(e){ return false; }
				var my_div = document.getElementById('sub');
				var div = document.createElement('div');
				div.setAttribute('class','form-group row');
				var new_select = document.createElement('select');
				new_select.setAttribute('id','select1');
				new_select.setAttribute('name', 'select1[]');
				div.appendChild(new_select);
				my_div.appendChild(div);
				new_select.multiple = true;
				new_select.setAttribute('size',10);
				//sessionStorage.setItem('active-table', 't_coalizione');
				dom.new_button(0, 'sub','b_edit_coalition', 'Inserisci Coalizione', listeners.button_set_alliance);//listeners.test_listener);
				localStorage.setItem('ally_is_set','n');	
			} else  {
					doAlert('alert', object.msg, 'index.php?action=new_record&t=partite');			
				}
			} else {
				dump.next('alleanza impostata, im in the callback');
				//doAlert('alert', 'Alleanza impostata, questo punto si ovrebbe proseguire');
				dom.do_msg('lead', object.msg);
				dom.dom_control();
				setOneCol('build-row');
				my_obj = object.table;
				dom.simple_list(my_obj, 'main', 'nazione', 'ul', 'li');//here!!!
				dom.new_button(0, 'main','b_select', 'Popola Tabelle', null);
			} 
				
	}
	
	var doGameTables = function(object,target){
		dom.do_msg('heading', 'Impostazione Tabelle');
		if(object.status === 0){
			dom.do_msg('lead', object.msg);
			/*dom.dom_control();
			setOneCol('build-row');
			var my_obj = object.table;
			dom.simple_list(my_obj, 'main', 'nazione', 'ul', 'li');	
			localStorage.setItem('ally_is_set','y');
			dom.do_msg('heading', 'Impostazione Tabelle Nazioni');*/	
		}
	}
	
	var getStorage = function(storage){
		if(localStorage.getItem(storage)){			
			return localStorage.getItem(storage);
		} else { return false; }		
	}
	
	var doInitControls = function(object, target, action){
		switch (object.type){
			case 'game':
				if(object.status === 1){
					window.location.href = 'index.php?action=select_ally&id_game=' + getStorage('id_game');
					return true;
				} else if (object.status === 0) {
					localStorage.removeItem('id_game');
					//window.location.href = 'index.php';
					main.do_ajax_all(new Array('action=select_game'));		
				}	
			break;
		}		
	}
	
	var appSupremacy = function(){
		var my_string_url;
		if(getStorage('id_game')){
			dump.next('id partita esistente!');
			my_string_url = new Array('action=do_init_controls', 'control=game', 'id_game=' + getStorage('id_game'));
			main.do_ajax_all(my_string_url);
			if(getStorage('ally_is_set') === 'y'){
				my_string_url = new Array('action=do_init_controls', 'control=alliance', 'id_game=' + getStorage('id_game'));	
				main.do_ajax_all(my_string_url);
			}
		} else {
			dump.next('id partita non esistente!');
			main.do_ajax_all(new Array('action=select_game'));
		}
	}
	
	
	return {
		do_auth: doAuth,
		app_supremacy: appSupremacy,
		do_init_controls: doInitControls,
		list_alliance: listAlliance,
		select_game: selectGame,		
		select_ally: selectAlly, 
		do_game_tables: doGameTables
		//my_test: myTest
	}
});

/*
var myTest = function(){
		var my_array = main.array_supremacy;
		main.my_app_function(my_array);
		myAppElement();
		if(!localStorage.getItem('id_game')){			
			dump.next('id partita non esistente!');
		} else {
			dump.next('id partita esistente!');
			//var my_string_url = new Array('action=do_init_controls','control=game','id_game=' + localStorage.getItem('id_game'));
			//do_ajax_all(my_string_url);
			main.launch_ajax('do_init_controls', 'id_game');
			dom.panel_title();			
			myAppElement('id_game');
			if(!localStorage.getItem('ally_is_set')){
				dump.next('alleanza non impostata');
			} else {
				dump.next('alleanza impostata, debug here?');
				dom.panel_title();				
				main.launch_ajax('do_game_tables', 'id_game');
			}
		}
	}
	
	
	var myTest_copia = function(){
		var my_array = main.array_supremacy;
		main.my_app_function(my_array);
		myAppElement();
		if(!localStorage.getItem('id_game')){			
			dump.next('id partita non esistente!');
		} else {
			dump.next('id partita esistente!');
			/* function do controls */
			/*
			var y = main.new_url_array('id_game', localStorage.getItem('id_game'), 'do_init_controls');
			main.do_ajax('do_init_controls', y);
			
			main.launch_ajax('id_game','do_init_controls');
			dom.panel_title();
			//main.do_ajax('get_response');
			/* old procedure 
			var x = main.new_url_array('id_game', localStorage.getItem('id_game'), 'select_ally');			
			main.do_ajax('select_ally', x);
			
			//myAppElement('id_game',localStorage.getItem('id_game'), 'select_ally');
			myAppElement('id_game');
			if(!localStorage.getItem('ally_is_set')){
				dump.next('alleanza non impostata');
			} else {
				dump.next('alleanza impostata, debug here?');
				dom.panel_title();
				/*
				var url = main.new_url_array('id_game', localStorage.getItem('id_game'), 'do_game_tables');
				main.do_ajax('do_game_tables', url);
				
				main.launch_ajax('id_game','do_game_tables');
			}
		}
		//test_oggetto();
	}	
	

//dom.do_msg('heading', 'Test nuova funzione');
//var my_obj = object['table'];
/*if(object.status === 1){
//doAlert('info', object.msg);//'selezione partita');			
return true;
} else  {			
return false;
//doAlert('alert', object.msg);			
}	*/

