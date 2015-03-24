$(document).ready(function(){
	$('#like').click(function(){
		var crawlid;
		crawlid = $(this).attr("data-crawlid");
		$.get('/pubcrawl/rate_crawl/', {crawl_id: crawlid}, function(data){
				   $('#score').html(data);
				   $('#like').hide();
		});
	});
});