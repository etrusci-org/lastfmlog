















<?php
/*** ------------------------------------------------------------------------------------
 * Use the local stats file
 * create with action 'stats'
 */
$statsFile = realpath(__DIR__.'/../app/data/stats.json');
$stats = file_get_contents($statsFile);
$stats = json_decode($stats, true);


/*** ------------------------------------------------------------------------------------
 * Use the local database
 * populate with action 'update'
 */
require 'database.class.php';

// Path to your database file
$databaseFile = realpath(__DIR__.'/../app/data/database.sqlite3');

// Query for results
$DB = new DatabaseSQLite3(dbFile: $databaseFile);
$DB->open();

$q = 'SELECT playHash, playTime, artist, track, album FROM trackslog ORDER BY playTime DESC LIMIT 1;';
$latestTrack = $DB->querySingle($q);

$DB->close();



// Website HTML output
?>
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LastfmLog : example/web.php</title>
</head>
<body>

    <h1>LastfmLog : example/web.php</h1>

    <h2>latest track in database</h2>
    <pre><?php print_r($latestTrack); ?></pre>

    <h2>total plays</h2>
    <?php print($stats['playsTotal']); ?>

    <h3>all stats file data</h3>
    <pre><?php print_r($stats); ?></pre>


</body>
</html>
