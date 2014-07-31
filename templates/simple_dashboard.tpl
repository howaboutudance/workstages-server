<!DOCTYPE html>
<html lang="en">
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<meta name="viewport" content="width=device-width, initial-scale=1">
    	<link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    	<title>Workstages Dashboard</title>
    </head>
    <body>
    	
    	<header class="navbar navbar-inverse navbar-fixed-top">
    		<div class="navbar-left">
        		<h1> WorkStages Dashboard </h1>
        	</div>
        	<button class="navbar-btn btn btn-default navbar-right">
        		Sign in
        	</button>
        	<ul class="side-nav">
	        		<li>General</li>
	        	</ul>
        </header>
        <aside class=" col-sm-3 col-md-3 sidebar-wrapper">
	        	
	    </aside>
        <section class="row">
	        
	        <section class="panel" id="stages">
		       	<h2 class="panel-heading">Stages</h2>
		        <article id="stages_list" class="panel-body">
		        	<table class="table table-striped">
		        		<thead>
			        		<tr>
			        			<th>time started</th>
			        			<th>interval</th>
			        			<th>type</th>
			        		</tr>
		        		</thead>
		        		<tbody class="main_data">
			        		<tr id="stages_template">
			        			<td class="time_started"></td>
			        			<td class="interval"></td>
			        			<td class="type"></td>
			        			<td><button class='btn btn-default'><span class="glyphicon glyphicon-remove"></span></button></td>
			        		</tr>
		        		</tbody>
		        	</table>
		        </article>
	        </section>
	        <section id="summary" class=panel>
	        	<h2 class="panel-heading">Summary</h2>
	        	<article>
	        		<ul class="list-group">
	        			<li class="list-group-item">Total Stages Completed:<span id="stages_total" class="stat_value"></span></li>
	        			<li class="list-group-item">Total Hours Worked:<span id="stages_worked" class="stat_value"></span></li>
	        			<li class="list-group-item">Total Hours on Break:<span id="stages_break" class="stat_value"></span></li>
	        		</ul>
	        	</article>
	        </section>
        </section>
        <footer>
        	<sub>&copy; Michael Penhallegon all rights reserved.</sub>
        </footer>
        <!-- jQuery  required -->
        <script src="static/js/jquery-2.1.1.min.js"></script>
        <script src="static/bootstrap/js/bootstrap.min.js"></script>
        <script>
        function addDeleteAction(id){
        	$("#"+id+" button").click(function(){
        							$.ajax({
	        							type:"DELETE",
	        							url:"entries/"+id,
	        							data: id,
	        							success: function(data){
	        								$("#"+id).css("visibility","hidden");
	        								$("#"+id).css("display","none")
	        							}
        							});
        						});
        };
        function refreshlist() {
        	$.getJSON (
        			"report/10",
        			function(data){
        				
        				
        				for(var i=0; i < data.length; i++) {
        					var row_template = $("#stages_template").clone();
        					var rowdata = data[i];
        					var new_id = rowdata['stage_id']
        					row_template.attr("id",new_id)
        					row_template.children(".time_started").text(new Date(rowdata['start_time']));
        					row_template.children(".type").text(rowdata['type']);
        					row_template.children(".interval").text(rowdata['interval']);
        					row_template.insertBefore("#stages_template");
        					addDeleteAction(new_id);
        					
        				}
        				$('#stages_template').css("visibility","hidden")
        			});
        	};
        	$(document).ready(function() {
        		$.getJSON (
        			"summary",
        			function(data){
        				var time_worked = 0;
        				var total_stages = 0;
        				var time_break = 0
        				time_worked = data['hours_worked']
        				total_stages = data['total_stages']
        				time_break = data['hours_break']
        				$("#stages_total").text(total_stages);
        				$('#stages_worked').text(Math.round(time_worked/60,4));
        				$("#stages_break").text(Math.round(time_break/60, 4));
        			})
        		refreshlist();
        		
        	});
        </script>
    </body>
</html>
