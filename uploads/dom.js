//document.getElementById(element)
dom = dom.createModule( function(){
	
	var testDom = function(target){
		if(document.getElementById(target)) alert('dom funzionante');
	};
	/* Response Object manipulation */
	var handleObj = function(response){
		this.obj = response;
		this.set_obj = function(){
			this.name = this[name];
			for(var s in this){
				this.name = this[s];
			}
		}
		this.call_names = function(){
			for(var i in this.obj){
		  	this.set_obj.call(this, this.set_obj[i]);			
		  }
		}
	}
	
	/* funzione di test per settare modularita */	
	
	/* dom strictly functions */
	var e = function(type,target){
		this.el = document.createElement(type);
		document.getElementById(target).appendChild(this.el);
	}
	e.prototype.inner = function(text){
		this.el.innerHTML = text;
	}
	e.prototype.set_a = function(a,b){
		return this.el.setAttribute(a,b);
	}
	
	e.prototype.add_class = function(a){
		return this.set_a('class',a);
		//return this.el.setAttribute(a,b);
	}
	
	/* test meesages */	
	var doMsg = function(div,msg){		
		var x = document.getElementById(div);
		x.innerHTML = msg;		
		return x;
	}
	
	
	/* create boostrap row content */
	var domControl = function(){
		dump.next('dom control');
		main.get_obj_storage();
		var my_query = getArrayStorage();
		var keys = returnArrayLength();
		/* dom control functions */
		setForm = function(){
			var form = new e ('form','build-row');
			form.set_a('id','my_form');
		}
		setOneCol = function(target){
			var my_div = document.getElementById(target);
			var div = document.createElement('div');
			div.setAttribute('class','col-lg-12');
			div.setAttribute('id','main');
			my_div.appendChild(div);
		};
		setTwoCols = function(size_col,target){
			var my_div = document.getElementById(target);
			var div = document.createElement('div');
			div.setAttribute('class','col-lg-' + size_col);
			div.setAttribute('id','main');
			my_div.appendChild(div);
			var calculate_size = 12 - size_col;
			var div2 = document.createElement('div');
			div2.setAttribute('class','col-lg-' + calculate_size);
			div2.setAttribute('id','sub');
			my_div.appendChild(div2);
		};
		setMainCols = function(target){
			if(keys == 1){
				setOneCol(target);
			}			
			else if (keys == 2){
				setTwoCols(8, target);
			}
		}
		/* end of fucntions, begin main function return */
		if(userObj.sections[my_query[0]].dom == 'n'){
			return false;	
		} else {
			if(userObj.sections[my_query[0]].is_form == 'y') {
				setForm();
				setMainCols('my_form');
			} else {
				setMainCols('build-row');
			}	
		}		
	}	
			/*if(!userObj.sections[my_query[0]].dom == 'n'){
				setMainCols('my_form');
			} /*
			else if (userObj.sections[my_query[0]].dom == 'n'){
				setMainCols('my_form');
			} 
			
			else {
			}				
						

	
	
	/* form functions */
	var panelTitle = function(){
		var x = document.getElementById('p_heading')
		x.innerHTML = '<b>ID Partita ' + localStorage.getItem('id_game') + '</b>';
	}	

	var doAlert = function(type, text , href){
		//{}	
		var div = new e('div','h5');
		if(type === 'alert'){
			div.add_class('alert alert-danger');	
		}	else if (type === 'info'){
			div.add_class('alert alert-info'); 
		}
		div.set_a('id', 'alert');
		dump.inspect(text);	
		div.inner(text);		
		if(arguments[2]){
			var link = new e ('a','alert');
			link.set_a('href', href);
			link.inner('  Clicca per inserire nuove partite');	
		}	
		
	}
	
	var newButton = function(offset, target, id, text, callback){
		var my_div = document.getElementById(target);
		var div = document.createElement('div');
		div.setAttribute('class','form-group row');
		var div1 = document.createElement('div');
		div1.setAttribute('class','col-xs-7 col-xs-offset-' + offset);
		var button = document.createElement('button');
		button.setAttribute('type', 'submit');
		button.setAttribute('id', id);
		button.setAttribute('class','btn btn-primary');
		button.innerHTML = text;
		div1.appendChild(button);
		div.appendChild(div1);
		my_div.appendChild(div);
		if(arguments[3]){
			listeners.new_listener(id, 'click', callback);
		}
	}
	
	/* active callbacks */
	
	/*
	var controlSomething = function(object, target, item){
		switch(item){
			case 'alliance':
				if(object.status === 1) return true;
				else return false;
			break;
		}		
	}
	*/
	
	var testObj = function(object, target, action){
		dom.do_msg('heading', 'Test nuova funzione');
		//var my_obj = object['table'];
		if(object.status === 1){
			doAlert('info', object.msg);//'selezione partita');						
		} else  {
			doAlert('alert', object.msg);			
		}	
	}
	
	var truncateTables = function(object, target, action){
		if(confirm("Stai procedendo allo svuotamento delle  tabelle di gioco, continuare?")){
			dom.do_msg('heading', 'Azzeramento Tabelle');
			//var my_obj = object['table'];
			if(object.status === 1){
				doAlert('info', object.msg);//'selezione partita');						
			} else  {
				doAlert('alert', object.msg);			
			}		
		}		
	}
		
	
	var simpleList = function(object, target, field_txt,  container, child){
		var div = document.getElementById(target);
		var my_div = document.createElement(container);
		var initObj = new handleObj(object);		
			for (var i in initObj.obj){
				initObj.call_names();			
				for (var y in initObj.obj[i]){
					var sub = document.createElement(child);
					sub.innerHTML = initObj.obj[i][field_txt];
					my_div.appendChild(sub);								
				}	
			}		
		div.appendChild(my_div);
	}
	
	
	
	var mainTable = function(object, target){
		//dump.inspect(object);
		var initObj = new handleObj(object);
		/* controllo se esiste un id settato 
		if(sessionStorage.getItem('my_id')){
			sessionStorage.removeItem('my_id');
			dump.next('rimosso id sessionStorage');
		}*/
		//setRowData();
		var div = document.getElementById(target);
		var t = document.createElement('table');
		t.setAttribute('id','my_table');
		t.setAttribute('class','table');
		/* thhead */
		var th = document.createElement('thead');
		var rh = document.createElement('tr');
		/* tfoot */
		var tf = document.createElement('tfoot');	
		var rf = document.createElement('tr');		
		for (var x in initObj.obj[0]){	
			/* thhead */		
			var dh = document.createElement('th');			
			var dht = document.createTextNode(x);
			dh.appendChild(dht);
			rh.appendChild(dh);
			/* tfoot */
			var df = document.createElement('td');
			var dft = document.createTextNode('tfoot');
			df.appendChild(dft);
			rf.appendChild(df);
		}
		/* thhead */
		th.appendChild(rh);
		t.appendChild(th);			
		/* tfoot */
		tf.appendChild(rf);
		t.appendChild(tf);
		/* tbody */
		var tb = document.createElement('tbody');
		//dump.next('debug: control dom');
		for (var i in initObj.obj){
			var r = document.createElement('tr');
			initObj.call_names();			
			for (var y in initObj.obj[i]){
				var d = document.createElement('td');
				var a_ = document.createElement('A');
				var obj_text = document.createTextNode(initObj.obj[i][y]);
				a_.appendChild(obj_text);				
				d.appendChild(a_);		
				r.appendChild(d);
				a_.href = userObj.cfg.index_file + '?action=view_record&t=' + userObj.cfg.default_table + '&id=' + initObj.obj[i]['id'];
			}
			tb.appendChild(r);
		}
		/* chiude tabella */
		t.appendChild(tb);
		/* appende child nel div */
		div.appendChild(t);		
	}
	
	var newRecord = function(object,target){
		//dom.dom_control();			
		//setOneCol('my_form');
		var initObj = new handleObj(object[0]);	
		var post_data = "";		
		var my_div = document.getElementById(target);				
		for (var i in initObj.obj){
			var div1 = document.createElement('div');			
			div1.setAttribute('class', 'form-group row');
			var label = document.createElement('label');
			label.setAttribute('class','col-xs-2 col-form-label');
			var obj_text = document.createTextNode(i);
			label.appendChild(obj_text);
			div1.appendChild(label);
			var div2 = document.createElement('div');			
			div2.setAttribute('class', 'col-xs-7');
			var input = document.createElement('input');
			input.setAttribute('class','form-control');
			input.setAttribute('type','text');
			input.setAttribute('name',i);
			input.setAttribute('value','');
			div2.appendChild(input);			
			div1.appendChild(div2);
			my_div.appendChild(div1);
			
		}
		newButton(2, 'main','b_insert','Inserisci', listeners.button_insert);
		/*
		createButton('submit','b_insert','Inserisci Nuovo', listnr.button_insert);
		main.new_listener('b_insert','click', main.button_insert);
		*/
	}
	
	var buildSelect = function(object,target,id_select,id,value,default_value){
		//setRowData();
		var my_div;
		if(!document.getElementById(target)) my_div = document.getElementById('main');
		else my_div = document.getElementById(target);	
		//var my_div = document.getElementById('main');
		var div = document.createElement('div');
		div.setAttribute('class','form-group row');
		var s = document.createElement('select');
		if(arguments[2]){
			s.setAttribute('id',id_select);
		} else s.setAttribute('id','my_select');		
		div.appendChild(s);
			option = function(value,txt){
			var my_option = document.createElement('option');
			my_option.value = value;
			my_option.text = txt;			
			s.add(my_option, null);		
		}
		if(arguments[5]){
			option(null, default_value);
		}
		var a = new handleObj(object);
		for (var i in a.obj){			
			a.call_names();
			//option(a.obj['id'],a.obj['nazione']);
			option(a.obj[i][id],a.obj[i][value]);
			/*for (var y in a.obj[i]){
				option(a.obj[i]['id'],a.obj[i]['nazione']);				
			}*/
		}
		my_div.appendChild(div);
		//dump.next('close section');		
	}
	
	/* old callbacks to reactivate */
	
	var viewRecord = function(object,target,id){
		var initObj = new handleObj(object[0]);				
		var div = document.getElementById(target);
		var form = document.createElement('FORM');		
		form.setAttribute("ID","my_form");
		var hidden = document.createElement('INPUT');
		hidden.setAttribute('TYPE', 'hidden');
		hidden.setAttribute('NAME','id');
		var table = document.createElement('TABLE');
		table.setAttribute("ID","my_table");
		var t_body = document.createElement('TBODY');
		for (var i in initObj.obj){
			var row_ = document.createElement('TR');
			var td1_ = document.createElement('TD');
			var name = i;
			var obj_text = document.createTextNode(name);							
			td1_.appendChild(obj_text);
			var td2_ = document.createElement('TD');
			var value = document.createTextNode(initObj.obj[i]);
			td2_.appendChild(value);
			row_.appendChild(td1_);
			row_.appendChild(td2_);
			t_body.appendChild(row_);			
		}
		table.appendChild(t_body);
		hidden.setAttribute('VALUE', initObj.obj.id);
		form.appendChild(hidden);
		form.appendChild(table);				
		div.appendChild(form);	
		//sessionStorage.setItem('my_id', initObj.obj.id);
		setIdPointer('edit', initObj.obj.id);					
	}	
	var editRecord = function(object,target,id){
		var initObj = new handleObj(object[0]);			
		var div = document.getElementById(target);
		var form = document.createElement('FORM');
		form.setAttribute("ID","my_form");
		var table = document.createElement('TABLE');
		table.setAttribute("ID","my_table");
		var t_body = document.createElement('TBODY');
		for (var i in initObj.obj){
			var row_ = document.createElement('TR');
			var td1_ = document.createElement('TD');
			var sub = i;
			var obj_text = document.createTextNode(sub);							
			td1_.appendChild(obj_text);
			var td2_ = document.createElement('TD');
			var input_ = document.createElement('INPUT');
			input_.setAttribute("TYPE","TEXT");
			input_.setAttribute("NAME","");
			input_.setAttribute("VALUE","");
			input_.size = 60;
			input_.name = sub;
			input_.defaultValue = initObj.obj[i];
			td2_.appendChild(input_);
			row_.appendChild(td1_);
			row_.appendChild(td2_);
			t_body.appendChild(row_);
		}
		table.appendChild(t_body);
		form.appendChild(table);				
		div.appendChild(form);
		/* add buttons */
		createButton('submit','b_edit','Aggiorna', listnr.button_edit);
		createButton('submit','b_delete','Elimina', listnr.button_delete);
		
	}
	
	/* old dom functions */
	
	var createDomList = function(){
		var ul = document.createElement("ul");
		ul.setAttribute("id","my_list");
		document.getElementById('_aside').appendChild(ul);
	}	
	var createDomSubList = function(link,text,id){
		var x= document.createElement('li');
		document.getElementById('my_list').appendChild(x);
		var a = document.createElement('a');
		a.setAttribute('href', link);		
		var b = document.createTextNode(text);
		a.setAttribute('id', id);
		a.appendChild(b);
		x.appendChild(a);		
	}
	
	return {
		test_dom: testDom,
		handle_obj: handleObj,
		element: e,
		do_msg: doMsg,		
		//do_main_msg: main_msg,
		dom_control: domControl,
		panel_title: panelTitle,
		do_alert: doAlert,
		new_button: newButton,
		simple_list: simpleList,
		create_list: createDomList,	
		create_link: createDomSubList,
		test_obj: testObj,
		truncate_tables: truncateTables,
		main_table: mainTable,
		build_select: buildSelect,
		/*select_multiple: selectMultiple,*/
		view_record: viewRecord,
		edit_record: editRecord,
		new_record: newRecord,		
		/*new_callback : newComplexCallback,*/			
	}	
});

var domControl_copia = function(){
	dump.next('dom control');
	var arrayReq = JSON.parse(sessionStorage.getItem("req"));
	var keys = Object.keys(arrayReq);
	setForm = function(){
		var form = new e ('form','build-row');
		form.set_a('id','my_form');
	}
	setOneCol = function(target){
		var target = document.getElementById(target);
		var div = document.createElement('div');
		div.setAttribute('class','col-lg-12');
		div.setAttribute('id','main');
		target.appendChild(div);
	};
	setTwoCols = function(size_col,target){
		var target = document.getElementById(target);
		var div = document.createElement('div');
		div.setAttribute('class','col-lg-' + size_col);
		div.setAttribute('id','main');
		target.appendChild(div);
		var calculate_size = 12 - size_col;
		var div2 = document.createElement('div');
		div2.setAttribute('class','col-lg-' + calculate_size);
		div2.setAttribute('id','sub');
		target.appendChild(div2);
	};
	setMainCols = function(target){
		if(keys.length == 1){
			setOneCol(target);				
		} else if (keys.length == 2){				
			setTwoCols(8, target);
		}
	}
	if(userObj.sections[arrayReq[0]].is_form == 'y') {			
		setForm();
		if(!userObj.sections[getArrayStorage()].dom == 'n'){
			setMainCols('my_form');
		} else if (userObj.sections[arrayReq[0]].dom == 'n'){
			setMainCols('my_form');
		} else {
			setMainCols('my_form');
		}
				
	} else {
		setMainCols('build-row');
	}			
	test = function(){
		if(userObj.sections[arrayReq[0]].is_form == 'y') alert('element is form');
	}		
	dump.inspect(arrayReq);
}



