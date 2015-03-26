$(document).ready(function(){
    
    $('#current_page').val(0); 

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
        //Reset element counter current_page for new filter.
        $('#current_page').val(0);
        var startat;
        startat = 0; 
        
        var crawl = $(".hiddenCrawls");
        var crawls = [];
        for (i=0; i < crawl.length; i++ ) {
            crawls.push(crawl[i].innerHTML.toString());
        }
        
        $.get('/pubcrawl/crawl_list/', {sort_by: sortby, crawls: crawls, start_at: startat}, function(data){
            $('#content').html(data);
        });
		
        $('ul.nav-pills li.active').removeClass('active');
        $(this).addClass('active');
    });
	
	$('.pager li').click(function(){
	    var sortby;
		sortby = $('ul.nav-pills li.active').attr("data-sorttype");
        startat = parseInt($('#current_page').val());
        
        var crawl = $(".hiddenCrawls");
        var crawls = [];
        for (i=0; i < crawl.length; i++ ) {
            crawls.push(crawl[i].innerHTML.toString());
        }
        
        if ($(this).attr("id") == "next"){
            startat = startat + 3;
            $('#current_page').val(startat); 
            $('#prev').removeClass('disabled');
        }
        
        if ($(this).attr("id") == "prev"){
            //Check if first element reached.
            if (startat <= 3){
                startat = 0;
                $('#current_page').val(startat);
                $(this).addClass('disabled');
            }
            else {
                startat -= 3;
                $('#current_page').val(startat); 
            }
        }
        
		$.get('/pubcrawl/crawl_list/', {sort_by: sortby, crawls: crawls, start_at: startat}, function(data){
            $('#content').html(data);
        });
	});
});