console.log('filter connected........')

$(document).ready(function(){
    $(".ajaxLoader").hide();
    $(".filter-checkbox,#priceFilterBtn").on('click',function(){
        ajaxCall();
    })

	$("#price_sorting, #rangeInput").on('change', function(){
	    ajaxCall();
	});

	function ajaxCall(){
	    console.log("checkbox clicked")
		var _filterObj={};
		var _minPrice=$('#maxPrice').attr('min');
		var _maxPrice=$('#maxPrice').val();
		var _price_range = $('#price_sorting').val();
		console.log("price", _price_range)

		_filterObj.price_range=_price_range;
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;
		$(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
		});

		_filterObj.category = $('#category').val();

		// Run Ajax
		$.ajax({
		    url: '/filter-data/',
			data:_filterObj,
			dataType:'json',
			beforeSend:function(){
                $(".ajaxLoader").show();
			},
			success:function(res){
				console.log(res);
                $("#filteredProducts").html(res.data);
                $(".ajaxLoader").hide();
			}
		});
	};


	// Filter Product According to the price
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min');
		var _max=$(this).attr('max');
		var _value=$(this).val();
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min);
			$(this).focus();
			$("#rangeInput").val(_min);
			return false;
		}
	});
});