<?php

    if(isset($_GET["id"]))
        $id = $_GET["id"];
    else
        $id = 1;
    $db = new PDO("sqlite:report_database.db");


    $data = $db->query("SELECT MAX(id) FROM alarm_system");

    $data = $data->fetch();
    $maxId = $data[0];

    if($maxId < $id)
        $id = $maxId;

    $data = $db->query("SELECT image FROM alarm_system WHERE id = $id");

    $data->bindColumn(1, $lob, PDO::PARAM_LOB);
    $data = $data->fetch(PDO::FETCH_BOUND);

    header("Content-Type: image/jpg");
    echo($lob);
?>