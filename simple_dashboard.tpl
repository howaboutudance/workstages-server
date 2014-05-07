<!DOCTYPE html>
<html lang="en">
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<meta name="viewport" content="width=device-width, initial-scale=1">
    	<link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    	
    	<header class="navbar navbar-inverse navbar-fixed-top">
        	<h1> WorkStages Dashboard </h1>
        </header>
        <section class="row">
	        <aside class=" col-sm-3 col-md-3 sidebar">
	        	<ul class="nav nav-sidebar">
	        		<li>General</li>
	        	</ul>
	        </aside>
	        <section class="panel" id="stages">
		       	<h2 class="panel-heading">Stages</h2>
		        <article id="stages_list" class="panel-body">
		        	<table class="table">
		        		<thead>
			        		<tr>
			        			<th>id</th>
			        			<th>type</th>
			        			<th>interval</th>
			        		</tr>
		        		</thead>
		        		<tbody>
			        		<tr id="stages_template">
			        			<td class="id"></td>
			        			<td class="type"></td>
			        			<td class="interval"></td>
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
        <script src="lib/jquery-2.0.3.js"></script>
        <script src="static/bootstrap/js/bootstrap.min.js"></script>
        <script>
        	$(document).ready(function() {
        		$.ajax ()
        		$("#stages_worked").text("temp_value");
        	});
        </script>
    </body>
</html>