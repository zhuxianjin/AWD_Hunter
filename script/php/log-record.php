<?php
date_default_timezone_set("Asia/Shanghai");

if (!function_exists('getallheaders')) {
    function getallheaders() {
    $headers = [];
    foreach ($_SERVER as $name => $value) {
        if (substr($name, 0, 5) == 'HTTP_') {
            $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value;
        }
    }
        return $headers;
    }
    
}


function WAF_log() {
global $WAF_query, $WAF_headers, $WAF_post, $WAF_log;
$tmp  = "[" . date('y-m-d H:i:s') . "]\n";
$tmp .= "SRC IP: " . $_SERVER["REMOTE_ADDR"]."\n";
$tmp .= $_SERVER['REQUEST_METHOD'].''.'http://'.$_SERVER['SERVER_NAME'].':'.$_SERVER["SERVER_PORT"].$_SERVER["REQUEST_URI"]."\n";

foreach($WAF_headers as $k => $v) {
if($k=='Accept-Encoding'||$k=='Accept-Language'||$k=='Accept'||$k=='User-Agent'||$k=='Referer'||$k=='Cookie'||$k=='X-Forwarded-For')
$tmp .= $k . ': ' . $v . "\n";
}
if (!empty($WAF_post)) {
$tmp .= "\n". $WAF_post . "\n";
}
$tmp .= "\n";
@file_put_contents($WAF_log."log_".date("H",time()), $tmp, FILE_APPEND);
}

$WAF_query = $_SERVER['QUERY_STRING'];
$WAF_headers = getallheaders();
$WAF_post = @file_get_contents('php://input');
$WAF_log = '/tmp/';
$WAF_AD_log = '';

WAF_log();
?>
