USE photoapp;

INSERT INTO 
  users(email, lastname, firstname, bucketfolder)
  VALUES
  ('steven@gmail.com',	'gu',	'steven', 
    'aa278699-eea2-4428-9c21-ad83908e523d'),
  ('jenna@gmail.com', 'lee',	'jenna', 
    '93389dec-c6c2-4a24-a071-55ba881aae24'),
  ('johnwick@gmail.com', 'wick',	'john',
  	'6b9e2853-d7c7-440e-a5a4-89397188c72d'),
  ('ganon@gmail.com', 'dorf', 'ganon', 
    'test');
INSERT INTO 
  assets(userid, assetname, bucketkey)
  VALUES
  (80001,
    'kermit-headset.jpg',
    'aa278699-eea2-4428-9c21-ad83908e523d/e5ec9b22-82f9-4ab0-8cde-212a0df8e886.jpg'
    ),
  (80001,
    'mc-skin.jpg',
    'aa278699-eea2-4428-9c21-ad83908e523d/19bb64f7-f82e-492e-ac91-506bba1565fe.jpg'
    ),
  (80002,
    'cute-anime-girl.jpg',
    '93389dec-c6c2-4a24-a071-55ba881aae24/4402fd90-9e1f-48c1-8b93-095a4c7ab35f.jpg'
    ),
  (80002,
    'JapaneseGoblins.jpg',
    '93389dec-c6c2-4a24-a071-55ba881aae24/3d031e1e-04cc-4d64-9f77-9316aecd47d5.jpg'
    ),
  (80003,
    'square-watermelons.jpg',
    '6b9e2853-d7c7-440e-a5a4-89397188c72d/36e42859-2552-443c-93ce-bd948bd4e127.jpg'
    ),
  (80003,
    'minecraft-lego.jpg',
    '6b9e2853-d7c7-440e-a5a4-89397188c72d/80a9e257-eed1-43f5-a501-29348b91e9b8.jpg'
    ),
  (80004,
    'spike.jpg',
    'test/f9e6ae40-e3d1-4964-9758-9d460db215c4.jpg'
    ), 
  (80004,
    'ganondorf-jumpscare.jpg',
    'test/4712009f-3ad6-41a1-8aec-1d509b7c5891.jpg'
    );