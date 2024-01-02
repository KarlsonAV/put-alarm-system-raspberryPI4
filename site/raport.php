<!DOCTYPE html>
<html lang="pl">
    <head>
        <meta charset="utf-8">
        <title>System alarmowy</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <header>
            <a href='index.php'><h1>System alarmowy</h1></a>
        </header>
        <main>
        <?php
            if(isset($_POST["date"]))
            {
                echo "<p>".$_POST["date"]."</p>";
                $db = new PDO("sqlite:report_database.db");

                $incidents = $db->query("SELECT id, DATE FROM alarm_system WHERE DATE LIKE '".$_POST["date"]."%'");
                $incidents = $incidents->fetchAll(PDO::FETCH_ASSOC);
                $elem = count($incidents);
                echo "<hr>";
                for($i = 0;$i < $elem; $i++)
                {
                    $time = explode(" ",$incidents[$i]["DATE"]);
                    $time = explode(".",$time[1]);
                    if(0 == $i%2)
                        echo "<div class='incident0'>";
                    else
                        echo "<div class='incident1'>";
                    echo "<div class='id'>";
                    echo "<p class='pRaport'>".strval($i+1).".</p>";
                    echo "</div>";
                    echo "<div class='foto'>";
                    echo "<img src='image.php?id=".$incidents[$i]["id"]."'>";
                    echo "</div>";
                    echo "<div class='time'>";
                    echo "<p class='pRaport'>".$time[0]."</p>";
                    echo "</div>";
                    echo "</div>";
                    echo "<hr>";
                }
            }
            
        ?>
        </main>
    </body>
</html>