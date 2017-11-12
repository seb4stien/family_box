<?php

function genCatalog($dir, &$res) {
	$content = scandir($dir);

	$goodContent = array();

	foreach ($content as $key => $value) {
		if (substr($value, 0, 1) != '.') {
			$path = $dir.'/'.$value;
			$rpath = substr($path, 11, 100);
			if (is_dir($path)) {
				$sub = genCatalog($path, $res);
				if ($sub) {
					$res[$rpath] = $sub;
					$goodContent[] = $value;
				}
			} else {
				$goodContent[] = basename($rpath, '.mp4');
			}
		}
	}

	return $goodContent;
}

$res = array();
$res['/mnt/media'] = genCatalog("/mnt/media", $res);
//print_r($res);

header('Content-Type: text/javascript');
print("var catalog = ".json_encode($res['/mnt/media'], JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE).";");
print("var detailedCatalog = ".json_encode($res,  JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE).";");

?>
