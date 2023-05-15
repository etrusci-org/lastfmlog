<?php
// ------------------------------------------------------------------
// Generate stats file with `cli.py stats` and then adjust this path
// so it points to your file:

const STATSFILE = __DIR__.'/../data/stats.json';

// ------------------------------------------------------------------


?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <title>LastfmLog - web example</title>
</head>
<body>
    <main class="container">
        <?php
        if (!is_file(STATSFILE)) {
            print('<p>stats file not found</p>');
            return;
        }
        else {
            $stats = file_get_contents(STATSFILE);
            $stats = json_decode($stats, true);
        }
        ?>

        <article>
            <h2>Overview</h2>
            <p>
                Stats updated on: <?php print(date('Y-m-d H:i:s T', $stats['_statsUpdatedOn'])); ?><br>
                Database updated on: <?php print($stats['_databaseUpdatedOn']); ?><br>
                Stats results limit: <?php print($stats['_resultsLimit']); ?>
            </p>
            <div class="grid">
                <div><strong><?php print($stats['totalScrobblesCount']); ?></strong> total scrobbles</div>
                <div><strong><?php print($stats['uniqueArtistsCount']); ?></strong> unique artists</div>
                <div><strong><?php print($stats['uniqueTracksCount']); ?></strong> unique tracks</div>
                <div><strong><?php print($stats['uniqueAlbumsCount']); ?></strong> unique albums</div>
            </div>
        </article>

        <div class="grid">
            <article>
                <h3>Yearly Playcounts</h3>
                <?php
                foreach ($stats['yearlyScrobblesCount'] as $v) {
                    printf('%1$s&nbsp;&nbsp;&nbsp;&nbsp;%2$s<br>',
                        $v['year'],
                        $v['count'],
                    );
                }
                ?>
            </article>

            <article>
                <h3>Monthly Playcounts</h3>
                <?php
                foreach ($stats['monthlyScrobblesCount'] as $v) {
                    printf('%1$s&nbsp;&nbsp;&nbsp;&nbsp;%2$s<br>',
                        $v['month'],
                        $v['count'],
                    );
                }
                ?>
            </article>

            <article>
                <h3>Daily Playcounts</h3>
                <?php
                foreach ($stats['dailyScrobblesCount'] as $v) {
                    printf('%1$s&nbsp;&nbsp;&nbsp;&nbsp;%2$s<br>',
                        $v['day'],
                        $v['count'],
                    );
                }
                ?>
            </article>
        </div>

        <article>
            <h3>Top Artists By Playcounts</h3>
            <table>
                <thead>
                    <tr>
                        <th>rank</th>
                        <th>artist</th>
                        <th>playcount</th>
                    </tr>
                </thead>
                <?php
                $rank = 1;
                foreach ($stats['topArtists'] as $v) {
                    printf('
                        <tr>
                            <td>%1$s</td>
                            <td>%2$s</td>
                            <td>%3$s</td>
                        </tr>',
                        $rank++,
                        $v['artist'],
                        $v['count'],
                    );
                }
                ?>
            </table>
        </article>

        <article>
            <h3>Top Tracks By Playcounts</h3>
            <table>
                <thead>
                    <tr>
                        <th>rank</th>
                        <th>track</th>
                        <th>artist</th>
                        <th>playcount</th>
                    </tr>
                </thead>
                <?php
                $rank = 1;
                foreach ($stats['topTracks'] as $v) {
                    printf('
                        <tr>
                            <td>%1$s</td>
                            <td>%2$s</td>
                            <td>%3$s</td>
                            <td>%4$s</td>
                        </tr>',
                        $rank++,
                        $v['track'],
                        $v['artist'],
                        $v['count'],
                    );
                }
                ?>
            </table>
        </article>

        <article>
            <h3>Top Albums By Playcounts</h3>
            <table>
                <thead>
                    <tr>
                        <th>rank</th>
                        <th>album</th>
                        <th>artist</th>
                        <th>playcount</th>
                    </tr>
                </thead>
                <?php
                $rank = 1;
                foreach ($stats['topAlbums'] as $v) {
                    printf('
                        <tr>
                            <td>%1$s</td>
                            <td>%2$s</td>
                            <td>%3$s</td>
                            <td>%4$s</td>
                        </tr>',
                        $rank++,
                        $v['album'],
                        $v['artist'],
                        $v['count'],
                    );
                }
                ?>
            </table>
        </article>
    </main>


    <footer class="container">
        <p><a href="https://github.com/etrusci-org/lastfmlog/#readme">what is this?</a></p>
    </footer>
</body>
</html>
