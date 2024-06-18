const fs = require('fs');
const path = require('path');
const connection = require('../config/connection');

const batikData = [
    {
        batikName: "Bali_Barong",
        batikDesc: "Motif ini menggambarkan sosok Barong, makhluk mitos dalam budaya Bali yang melambangkan kekuatan dan kesaktian. Biasanya menggunakan warna-warna cerah dan berani, seperti merah, kuning, dan hitam. Batik Barong sering dipakai dalam upacara adat dan ritual keagamaan.",
        imagePath: "src/images/Bali_Barong.jpg"
    },
    {
        batikName: "Bali_Merak",
        batikDesc: "Motif ini menampilkan burung merak, yang melambangkan keindahan, keanggunan, dan keabadian. Batik Merak biasanya menggunakan warna-warna cerah seperti biru, hijau, dan ungu, dengan detail bulu merak yang rumit dan indah. Batik ini sering dipakai dalam acara-acara resmi dan pernikahan.",
        imagePath: "src/images/Bali_Merak.jpg"
    },
    {
        batikName: "DKI_Ondel_Ondel",
        batikDesc: "Motif ini terinspirasi dari boneka Ondel-ondel, ikon budaya Betawi yang khas. Batik Ondel-onde biasanya menggunakan warna-warna cerah dan ceria, seperti merah, kuning, dan biru, dengan gambar boneka Ondel-ondel yang besar dan mencolok. Batik ini sering dipakai dalam acara-acara budaya dan festival di Jakarta.",
        imagePath: "src/images/DKI_Ondel_Ondel.jpg"
    },
    {
        batikName: "JawaBarat_Megamendung",
        batikDesc: "Motif ini menggambarkan awan mendung yang menyelimuti langit, melambangkan kekuatan alam dan kesabaran. Batik Megamendung biasanya menggunakan warna-warna biru tua dan hitam, dengan corak awan yang meliuk-liuk. Batik ini sering dipakai dalam acara-acara formal dan resmi.",
        imagePath: "src/images/JawaBarat_Megamendung.jpg"
    },
    {
        batikName: "JawaTimur_Pring",
        batikDesc: "Motif ini menampilkan pohon bambu, melambangkan kesederhanaan, kekuatan, dan kelenturan. Batik Pring biasanya menggunakan warna-warna hijau dan coklat, dengan corak batang bambu yang ramping dan daun bambu yang menari-nari. Batik ini sering dipakai dalam acara-acara sehari-hari dan kasual.",
        imagePath: "src/images/JawaTimur_Pring.jpg"
    },
    {
        batikName: "Kalimantan_Dayak",
        batikDesc: "Motif ini terinspirasi dari budaya suku Dayak di Kalimantan, yang kaya akan corak dan simbol-simbol adat. Batik Dayak biasanya menggunakan warna-warna cerah dan berani, seperti merah, kuning, dan hitam, dengan corak hewan hutan, motif abstrak, dan ukiran khas Dayak. Batik ini sering dipakai dalam upacara adat dan ritual keagamaan.",
        imagePath: "src/images/Kalimantan_Dayak.jpg"
    },
    {
        batikName: "Madura_Mataketeran",
        batikDesc: "Motif ini menggambarkan mata kerbau, melambangkan kewaspadaan, kehati-hatian, dan ketekunan. Batik Mataketeran biasanya menggunakan warna-warna coklat dan hitam, dengan corak mata kerbau yang besar dan mencolok. Batik ini sering dipakai dalam acara-acara formal dan resmi.",
        imagePath: "src/images/Madura_Mataketeran.jpg"
    },
    {
        batikName: "Maluku_Pala",
        batikDesc: "Motif ini menampilkan buah pala, yang merupakan salah satu rempah-rempah khas Maluku. Batik Pala biasanya menggunakan warna-warna coklat dan putih, dengan corak buah pala yang detail dan realistis. Batik ini sering dipakai sebagai souvenir dan hadiah dari Maluku.",
        imagePath: "src/images/Maluku_Pala.jpg"
    },
    {
        batikName: "Papua_Asmat",
        batikDesc: "Motif ini terinspirasi dari seni ukir suku Asmat di Papua, yang terkenal dengan corak dan simbol-simbol adat yang unik. Batik Asmat biasanya menggunakan warna-warna coklat dan hitam, dengan corak patung dan ukiran khas Asmat yang rumit dan indah. Batik ini sering dipakai dalam upacara adat dan ritual keagamaan.",
        imagePath: "src/images/Papua_Asmat.jpg"
    },
    {
        batikName: "Papua_Cendrawasih",
        batikDesc: "Motif ini menggambarkan burung Cendrawasih, yang merupakan ikon Papua yang melambangkan keindahan, kebebasan, dan kebahagiaan. Batik Cendrawasih biasanya menggunakan warna-warna cerah dan ceria, seperti merah, kuning, dan biru, dengan gambar burung Cendrawasih yang menari-nari di antara pepohonan. Batik ini sering dipakai dalam acara-acara budaya dan festival di Papua.",
        imagePath: "src/images/Papua_Cendrawasih.jpg"
    },
    {
        batikName: "Papua_Tifa",
        batikDesc: "Motif ini menampilkan alat musik tradisional Papua yang disebut Tifa, yang melambangkan semangat, kebersamaan, dan kegembiraan. Batik Tifa biasanya menggunakan warna-warna coklat dan hitam, dengan corak Tifa yang detail dan realistis. Batik ini sering dipakai dalam acara-acara adat dan ritual keagamaan.",
        imagePath: "src/images/Papua_Tifa.jpg"
    },
    {
        batikName: "Solo_Parang",
        batikDesc: "Motif ini terkenal dengan corak garis-garis diagonal yang tajam, melambangkan keberanian, kekuatan, dan ketegasan. Batik Parang biasanya menggunakan warna-warna coklat dan hitam, dengan variasi motif parang yang beragam, seperti parang grid, parang klitik, dan parang salira. Batik ini sering dipakai dalam acara-acara formal dan resmi, terutama oleh para pria.",
        imagePath: "src/images/Solo_Parang.jpg"
    },
    {
        batikName: "Yogyakarta_Kawung",
        batikDesc: "Motif ini menampilkan bentuk kawung (kolang-kaling) yang tersusun rapi, melambangkan kesatuan, keseimbangan, dan kesempurnaan. Batik Kawung biasanya menggunakan warna-warna coklat dan putih, dengan variasi motif kawung yang beragam, seperti kawung pecah, kawung sri, dan kawung luncu. Batik ini sering dipakai dalam acara-acara adat dan ritual keagamaan, dan juga merupakan motif batik Yogyakarta yang paling terkenal.",
        imagePath: "src/images/Yogyakarta_Kawung.jpg"
    },
    {
        batikName: "SulawesiSelatan_Lontara",
        batikDesc: "Motif ini terinspirasi dari aksara Lontara, aksara tradisional Bugis yang unik dan indah. Batik Lontara biasanya menggunakan warna-warna coklat dan putih, dengan corak aksara Lontara yang tersusun rapi dan artistik. Batik ini sering dipakai dalam acara-acara adat dan ritual keagamaan, dan juga merupakan salah satu ciri khas budaya Bugis.",
        imagePath: "src/images/SulawesiSelatan_Lontara.jpg"
    },
    {
        batikName: "SumateraUtara_Boraspati",
        batikDesc: "Motif ini menggambarkan pohon Boras, yang merupakan pohon khas Sumatera Utara. Batik Boraspat biasanya menggunakan warna-warna coklat dan hitam, dengan corak pohon Boras yang detail dan realistis. Batik ini sering dipakai dalam acara-acara adat dan ritual keagamaan, dan juga merupakan salah satu ciri khas budaya Batak.",
        imagePath: "src/images/SumateraUtara_Boraspati.jpg"
    }
];

const sendImageBatikByBatikName = () => {
    batikData.forEach((batik) => {
        // Baca gambar dan convert ke base64
        const batikImg = fs.readFileSync(path.resolve(batik.imagePath)).toString('base64');

        // Insert data ke database
        const query = 'INSERT INTO batik (batikName, batikImg, batikDesc) VALUES (?, ?, ?)';
        connection.query(query, [batik.batikName, batikImg, batik.batikDesc], (err, results) => {
            if (err) {
                console.error('Error inserting data:', err);
            } else {
                console.log(`Batik ${batik.batikName} inserted successfully`);
            }
        });
    });
};

sendImageBatikByBatikName();
