<?php
$statsFile = realpath(__DIR__.'/../app/data/stats.json');
$stats = file_get_contents($statsFile);
$stats = json_decode($stats, true);
?>
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LastfmLog : example/php-stats-json.php</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
</head>
<body>
    <div class="container">

        <h1><a href="https://github.com/etrusci-org/lastfmlog#readme">LastfmLog</a> : example/php-stats-json.php</h1>


        <p>
            Statistics last updated on: <?php print(date('Y-m-d H:i:s', $stats['_statsUpdatedOn'])); ?><br>
            Database last updated on: <?php print(date('Y-m-d H:i:s', $stats['_databaseUpdatedOn'])); ?><br>
            Data range: <?php print(date('Y-m-d H:i:s', $stats['firstPlayTime'])); ?> - <?php print(date('Y-m-d H:i:s', $stats['latestPlayTime'])); ?><br>
            <em>All times are in UTC</em>
        </p>


        <h2>Totals</h2>
        <ul>
            <li><strong><?php print($stats['playsTotal']); ?></strong> plays</li>
            <li><strong><?php print($stats['uniqueArtists']); ?></strong> artists</li>
            <li><strong><?php print($stats['uniqueTracks']); ?></strong> tracks</li>
            <li><strong><?php print($stats['uniqueAlbums']); ?></strong> albums</li>
        </ul>


        <h2>Top 10 Artists by Plays</h2>
        <ol>
            <?php
            foreach ($stats['topArtists'] as $v) {
                printf('<li>(%1$s) <strong>%2$s</strong></li>',
                    $v['plays'],
                    htmlspecialchars($v['artist']),
                );
            }
            ?>
        </ol>


        <h2>Top 10 Tracks by Plays</h2>
        <ol>
            <?php
            foreach ($stats['topTracks'] as $v) {
                printf('<li>(%1$s) <strong>%3$s</strong> by %2$s</li>',
                    $v['plays'],
                    htmlspecialchars($v['artist']),
                    htmlspecialchars($v['track']),
                );
            }
            ?>
        </ol>


        <h2>Top 10 Albums by Plays</h2>
        <ol>
            <?php
            foreach ($stats['topAlbums'] as $v) {
                printf('<li>(%1$s) <strong>%3$s</strong> by %2$s</li>',
                    $v['plays'],
                    htmlspecialchars($v['artist']),
                    htmlspecialchars($v['album']),
                );
            }
            ?>
        </ol>

        <h2>Plays in Last 7 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays7days']['plays'],
            $stats['plays7days']['average'],
        );
        ?>


        <h2>Plays in Last 14 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays14days']['plays'],
            $stats['plays14days']['average'],
        );
        ?>


        <h2>Plays in Last 30 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays30days']['plays'],
            $stats['plays30days']['average'],
        );
        ?>


        <h2>Plays in Last 90 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays90days']['plays'],
            $stats['plays90days']['average'],
        );
        ?>


        <h2>Plays in Last 180 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays180days']['plays'],
            $stats['plays180days']['average'],
        );
        ?>


        <h2>Plays in Last 365 Days</h2>
        <?php
        printf('<p><strong>%1$s</strong> (average/day: %2$s)</p>',
            $stats['plays365days']['plays'],
            $stats['plays365days']['average'],
        );
        ?>

        <h2>Plays by Year</h2>
        <ul>
            <?php
            foreach ($stats['playsByYear'] as $v) {
                printf('<li>%2$s <strong>%1$s</strong></li>',
                    $v['plays'],
                    $v['year'],
                );
            }
            ?>
        </ul>


        <h2>Plays by Month</h2>
        <ul>
            <?php
            foreach ($stats['playsByMonth'] as $v) {
                    printf('<li>%2$s <strong>%1$s</strong></li>',
                    $v['plays'],
                    $v['month'],
                );
            }
            ?>
        </ul>


        <h2>Plays by Day</h2>
        <ul>
            <?php
            foreach ($stats['playsByDay'] as $v) {
                    printf('<li>%2$s <strong>%1$s</strong></li>',
                    $v['plays'],
                    $v['day'],
                );
            }
            ?>
        </ul>


        <h2>Plays by Hour</h2>
        <ul>
            <?php
            foreach ($stats['playsByHour'] as $v) {
                    printf('<li>%2$s <strong>%1$s</strong></li>',
                    $v['plays'],
                    $v['hour'],
                );
            }
            ?>
        </ul>
    </div>
</body>
</html>
