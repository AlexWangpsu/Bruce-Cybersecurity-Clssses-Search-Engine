<?php
/*
	Simple PHP call to the mongoDB client, which returns an array of info including unicount, profcount, and coursecount.
	It is necessary to json_encode this array and then echo it to the HTML code in index.html to parse.
*/
try {
    $mng = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $uni = new MongoDB\Driver\Command([
		'distinct' => 'mar1819courses',
		'key' => 'DOMAIN',
    ]);
    $prof = new MongoDB\Driver\Command([
		'distinct' => 'mar1819courses',
		'key' => 'PROF',
    ]);
    $courses = new MongoDB\Driver\Command([
		'distinct' => 'mar1819courses',
		'key' => 'URL',
    ]);

    $unicount = $mng -> executeCommand('users',$uni);
    $universities = current($unicount->toArray())->values;
    $profcount = $mng -> executeCommand('users',$prof);
    $professors = current($profcount->toArray())->values;
    $courcount = $mng -> executeCommand('users',$courses);
    $coursesall = current($courcount->toArray())->values;
    echo json_encode(array(count($coursesall),count($universities),count($professors)));

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
