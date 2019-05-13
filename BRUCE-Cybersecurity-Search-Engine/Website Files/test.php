
<?php
/*
	Creates a filter based on "projection" and "sort" to create a score that is used to rank the search results on how related it is to the search. Then, it also gets the rows from each column, puts them into an array, and sends them off.

*/
try {
    $mng = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $div = $_POST['title'];
    $curpage = $_POST['page'];
   
    $filter = [
    '$text' => ['$search' => $div]];
    $options =  [
    'projection' => [
        'score' => ['$meta' => 'textScore']
            ],
     'sort' => [
        'score' => ['$meta' => 'textScore']
        ]
    ];
    $mongoQuery = new MongoDB\Driver\Query($filter, $options);
    $cursor = $mng->executeQuery("users.mar1819courses",$mongoQuery);
    
    $i = 0;
    $total = array();
     
    $rowsperpage=10;
    foreach ($cursor as $row) {
    	$domain = $row -> DOMAIN;
    	$name =  $row -> PROF;
    	$title = $row -> TITLE;
		$content = $row -> CONTENT;
		$year = $row -> YEAR;
		$url = $row -> URL;
		$image = $row -> IMAGE;
		$score = $row -> score;
		$phone = $row -> PHONE;
		$email = $row -> EMAIL;
		$textbook = $row -> TEXTBOOK;
		$test = $row -> TEST;
		$i = $i+1;	
	
	$temp = array(
		domain => $domain,
		name => $name,
		title => $title,
		content => $content,
		year => $year,
		url => $url,
		phone => $phone,
		email => $email,
		textbook => $textbook,
		test => $test,
		image => $image,
		score => $score
	);
	//paginate here
	$numofpages = ceil($i/$rowsperpage);

	
	if($i<=($curpage)*10 and $i>($curpage-1)*10){
		$total[] = $temp;
	}	
}
    echo json_encode(array("arr"=>$total,"num"=>$i,"pages"=>$numofpages));    
}
catch (MongoDB\Driver\Exception\ConnectionTimeoutException $e)
{
    $filename = basename(__FILE__);

    echo "The $filename script has experienced an error.\n";
    echo "It failed with the following exception:\n";

    echo "Exception:", $e->getMessage(), "\n";
    echo "In file:", $e->getFile(), "\n";
    echo "On line:", $e->getLine(), "\n";
}
?>
