$(document).ready(function(){
	$('#like').click(function(){
		var crawlid;
		crawlid = $(this).attr("data-crawlid");
		$.get('/pubcrawl/rate_crawl/', {crawl_id: crawlid}, function(data){
				   $('#score').html(data);
				   $('#like').hide();
		});
	});
	
	$('ul.nav.nav-pills li').click(function(){
        var sortby;
        sortby = $(this).attr("data-sorttype");
        $.get('/pubcrawl/crawl_list/', {sort_by: sortby}, function(data){
            $('#content').html(data);
        });
		
        $('ul.nav-pills li.active').removeClass('active');
        $(this).addClass('active');
    });
});