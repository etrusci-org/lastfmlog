<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LastfmLog : example/php-stats-json.php</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
</head>
<body>
    <div class="container">
        <?php
        require 'database.class.php';

        $startDate = '2024-03-01';
        $endDate = '2024-05-31';
        $itemsLimit = 30;
        $databaseFile = realpath(__DIR__.'/../app/data/database.sqlite3');


        $startDateStamp = strtotime($startDate.' 00:00:00');
        $endDateStamp = strtotime($endDate.' 23:59:59');
        $DB = new DatabaseSQLite3(dbFile: $databaseFile);
        $DB->open();
        $topAlbums = $DB->query('
        SELECT COUNT(album) AS plays, album, CASE WHEN COUNT(DISTINCT artist) > 1 THEN "Various Artists" ELSE MIN(artist) END AS artist
        FROM trackslog
        WHERE album IS NOT NULL AND playTime BETWEEN :startDateStamp AND :endDateStamp
        GROUP BY album COLLATE NOCASE
        ORDER BY plays DESC
        LIMIT :limit;', [
            ['limit', $itemsLimit, SQLITE3_INTEGER],
            ['startDateStamp', $startDateStamp, SQLITE3_INTEGER],
            ['endDateStamp', $endDateStamp, SQLITE3_INTEGER],
        ]);
        $DB->close();
        // print_r($topAlbums);


        printf('<h1>Top %1$s albums %2$s - %3$s</h1>', $itemsLimit, $startDate, $endDate);

        print('
            <table>
                <thead>
                    <tr>
                        <th>rank</th>
                        <th>plays</th>
                        <th>album</th>
                        <th>artist</th>
                    </tr>
                </thead>
                <tbody>
        ');

        $rank = 1;
        foreach ($topAlbums as $v) {
            printf('
                <tr>
                    <td>%1$s</td>
                    <td>%2$s</td>
                    <td>%3$s</td>
                    <td>%4$s</td>
                </tr>',
                $rank,
                htmlspecialchars($v['plays']),
                htmlspecialchars($v['album']),
                htmlspecialchars($v['artist']),
            );
            $rank++;
        }

        print('
                </tbody>
            </table>
        ');
        ?>
    </div>

</body>
</html>
