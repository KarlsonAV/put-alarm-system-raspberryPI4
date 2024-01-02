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
            $db = new PDO("sqlite:report_database.db");

            $numberOfIncidents = $db->query("SELECT COUNT(id) FROM alarm_system");
            $numberOfIncidents = $numberOfIncidents->fetch();
            $numberOfIncidents = $numberOfIncidents[0];
            echo "<p>System alarmowy zarejestrował <b>$numberOfIncidents</b> incydentów.</p>";

            $daty = $db->query("SELECT DATE FROM alarm_system");
            $daty = $daty->fetchAll(PDO::FETCH_ASSOC);
            $elem = count($daty);
            $last = "";
            echo "<hr>";
            $j = 0;
            for($i = 0;$i < $elem;$i++)
            {
                $data = explode(" ",$daty[$i]["DATE"]);
                if($last == $data[0])
                    continue;
                if(0 == $j%2)
                    echo "<div class='incidents0'>";
                else
                    echo "<div class='incidents1'>";
                echo "<div class='date'>";
                echo $data[0];
                echo "</div>";
                $incidents = $db->query("SELECT COUNT(id) FROM alarm_system WHERE DATE LIKE'".$data[0]."%'");
                $incidents = $incidents->fetch();
                echo "<div class='info'>";
                echo "<br> Incydentów: ".$incidents[0];
                $faces = $db->query("SELECT COUNT(id) FROM alarm_system WHERE DATE LIKE'".$data[0]."%' AND Faces = 1");
                $faces = $faces->fetch();
                echo "<br> Zdjęcia na których wykryto twarz: ".$faces[0];
                echo "</div>";
                echo "<div class='buttons'>";
                echo "<form method='POST' action='raport.php'> <input type='hidden' id='name' name='date' value='".$data[0]."'> <input type='submit' value='Zdjęcia z incydentów'> </form>";
                echo "<form method='POST' action='raport-faces.php'> <input type='hidden' id='name' name='date' value='".$data[0]."'> <input type='submit' value='Zdjęcia z incydentów, na których wykryto twarz'> </form>";
                echo "</div>";
                echo "</div>";
                $last = $data[0];
                $j++;
                echo "<hr>";
            }
        ?>
        </main>
    </body>
</html>
