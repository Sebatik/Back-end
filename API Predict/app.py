from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import efficientnet.keras as efn
from tensorflow.keras import backend, layers
from tensorflow.keras.models import load_model

app = Flask(__name__)

class FixedDropout(layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape

        symbolic_shape = backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape
                       for axis, shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)

# Load model with custom FixedDropout layer
model = load_model('model/raw_batik_v2.1_EfficientNetB3_epoch_70.h5', 
                   custom_objects={'FixedDropout': FixedDropout(rate=0.2)})

# Define class names according to what you obtained from the collab result
class_names = [
    'Bali_Barong', 'Bali_Merak','DKI_Ondel_Ondel','JawaBarat_Megamendung',
    'JawaTimur_Pring', 'Kalimantan_Dayak', 'Madura_Mataketeran',
    'Maluku_Pala', 'Papua_Asmat', 'Papua_Cendrawasih', 'Papua_Tifa',
    'Solo_Parang', 'SulawesiSelatan_Lontara', 'SumateraUtara_Boraspati', 'Yogyakarta_Kawung'
]

class_desc = [
    'Batik Bali motif Barong merupakan salah satu warisan budaya Bali yang memukau, menampilkan kekayaan budaya pulau Dewata ini. Motifnya terinspirasi dari Barong, makhluk mitologis yang melambangkan kebaikan, perlindungan, dan kekuatan spiritual dalam budaya Bali. Batik ini telah diwariskan dari generasi ke generasi, menjadi bukti nyata pelestarian budaya Bali yang kaya.\n\nProses pembuatan Batik Bali motif Barong mengikuti langkah-langkah tradisional membatik. Kain katun dipersiapkan untuk dicelup dalam larutan pewarna. Motif Barong kemudian digambar pada kain menggunakan malam (lilin) untuk menahan warna pada bagian tertentu, sehingga motif Barong yang indah terbentuk. Setelah proses pewarnaan selesai, lilin dilelehkan untuk mengungkapkan motif yang diinginkan. Tahap akhir adalah pencucian kain untuk menghilangkan lilin dan proses finishing lainnya.\n\nMotif Barong dalam batik ini memiliki makna filosofis yang mendalam. Dalam budaya Bali, Barong melambangkan kekuatan spiritual dan perlindungan. Kehadirannya dalam batik dapat dilihat sebagai bentuk penghormatan terhadap nilai-nilai tradisional Bali yang kaya. Batik Bali motif Barong juga menjadi sarana untuk memperkenalkan kekayaan budaya Bali kepada dunia dan mempromosikan nilai-nilai positif yang terkandung dalam budaya Bali, seperti kebaikan, perlindungan, dan kekuatan spiritual.\n\nSecara keseluruhan, Batik Bali motif Barong bukan hanya sebuah karya seni yang indah, tetapi juga merupakan perwujudan budaya dan spiritualitas yang kaya dari Bali. Batik ini tidak hanya menjadi kebanggaan masyarakat Bali, tetapi juga menjadi warisan budaya Indonesia yang patut dijaga dan dilestarikan.',

    'Batik Bali motif Merak merupakan salah satu kekayaan budaya Bali yang mempesona. Akar sejarahnya tidak bisa ditelusuri secara pasti, namun Batik Bali motif Merak telah menjadi bagian penting dari kehidupan dan seni di Bali selama bertahun-tahun. Keindahan motif Merak dan maknanya yang kaya menjadikannya favorit dalam industri batik Bali.n/Proses pembuatan Batik Bali motif Merak mengikuti langkah-langkah tradisional membatik. Kain katun dipersiapkan untuk dicelup dalam larutan pewarna. Motif Merak kemudian diaplikasikan pada kain menggunakan malam (lilin) untuk menahan warna pada bagian tertentu, sehingga motif Merak terbentuk dengan indah. Setelah proses pewarnaan selesai, lilin dilelehkan untuk mengungkapkan motif yang diinginkan. Tahap selanjutnya adalah pencucian kain untuk menghilangkan lilin dan proses finishing untuk menghasilkan batik yang menawan.\n\nBatik Bali motif Merak memiliki makna dan filosofi yang mendalam. Burung merak dalam budaya Bali sering dianggap sebagai simbol keindahan, kemewahan, dan keanggunan. Kehadirannya dalam batik dapat diartikan sebagai upaya untuk mengekspresikan keindahan alam dan kehidupan. Selain itu, burung merak juga dapat memiliki makna spiritual yang dalam, sering dikaitkan dengan kepercayaan dan mitos dalam budaya Bali.\n\nOleh karena itu, Batik Bali motif Merak bukan hanya sebuah karya seni yang indah, tetapi juga merupakan perwujudan keindahan alam dan budaya Bali yang kaya. Melalui batik ini, nilai-nilai keindahan, keanggunan, dan spiritualitas Bali dapat dipelajari dan diapresiasi oleh masyarakat luas. Batik Bali motif Merak menjadi pengingat akan kekayaan budaya Bali yang tak ternilai dan patut dilestarikan.',

    'Batik Ondel-Ondel merupakan salah satu jenis batik khas Betawi yang memiliki motif unik terinspirasi dari boneka raksasa tradisional Betawi, yaitu ondel-ondel. Batik ini tidak memiliki catatan sejarah yang pasti, namun keberadaannya telah menjadi bagian dari warisan budaya Betawi yang diwariskan dari generasi ke generasi.\n\nProses pembuatan Batik Ondel-Ondel pada dasarnya sama dengan batik pada umumnya. Kain katun dipersiapkan untuk dicelup dalam larutan pewarna. Motif ondel-ondel kemudian diaplikasikan pada kain menggunakan malam (lilin) untuk menahan warna pada bagian tertentu, sehingga motif ondel-ondel terbentuk. Setelah proses pewarnaan selesai, lilin dilelehkan untuk mengungkapkan motif yang diinginkan. Proses selanjutnya adalah pencucian kain untuk menghilangkan lilin dan proses-proses finishing lainnya.\n\nLebih dari sekadar motif batik, Batik Ondel-Ondel memiliki filosofi yang mendalam. Ondel-ondel melambangkan kegembiraan, semangat, dan kehidupan yang penuh warna dari masyarakat Betawi. Kehadiran motif ondel-ondel dalam batik juga menjadi bagian dari upaya untuk melestarikan budaya dan tradisi Betawi yang kaya. Batik Ondel-Ondel mengandung nilai-nilai budaya dan tradisi yang penting bagi masyarakat Betawi dan menjadi sarana untuk memperkenalkan kekayaan budaya mereka kepada dunia.\n\nBatik Ondel-Ondel biasanya hadir dalam dua versi, yaitu Bujang dan Nyi Onthel. Bujang melambangkan laki-laki dengan wajah merah dan Nyi Onthel melambangkan perempuan dengan wajah putih. Batik ini sering digunakan dalam berbagai acara adat dan budaya Betawi, seperti pernikahan, festival, dan pertunjukan seni.\n\nBatik Ondel-Ondel dapat menjadi souvenir atau hadiah yang menarik bagi orang terkasih. Anda juga dapat mempelajari lebih lanjut tentang Batik Ondel-Ondel dengan mengunjungi museum atau galeri seni di Jakarta yang memamerkan batik Betawi.',

    'Batik Jawa Barat motif Mega Mendung merupakan salah satu warisan budaya Cirebon yang tak ternilai. Motif ini berasal dari daerah Cirebon, Jawa Barat, Indonesia dan telah menjadi ikonik dalam seni batik Cirebon, melambangkan kekayaan budaya dan tradisi daerah tersebut. Sejarahnya dapat ditelusuri kembali ke masa lampau, di mana Batik Mega Mendung telah menjadi bagian penting dari kehidupan masyarakat Cirebon.\n\nProses pembuatan Batik Mega Mendung mengikuti teknik tradisional membatik. Kain katun dipersiapkan untuk dicelupkan ke dalam larutan pewarna. Motif Mega Mendung kemudian diaplikasikan pada kain menggunakan teknik canting atau cap untuk menciptakan pola awan yang berlapis-lapis, menyerupai mega mendung yang menawan. Setelah proses pewarnaan selesai, kain dicuci untuk menghilangkan lilin dan pewarnaan berlebih, sehingga motif Mega Mendung tampak jelas dan indah.\n\nUpaya pelestarian Batik Mega Mendung terus dilakukan melalui berbagai kegiatan, seperti pelatihan pengrajin batik muda, pameran dan workshop batik, serta promosi di platform online dan offline. Dengan membeli dan menggunakan Batik Mega Mendung, Anda turut mendukung para pengrajin batik lokal, membantu dalam melestarikan budaya Cirebon, dan membawa keindahan alam dan makna filosofisnya kepada generasi mendatang.\n\nBatik Mega Mendung dapat digunakan untuk berbagai acara, seperti acara formal, semi-formal, dan kasual. Anda juga dapat menggunakan batik ini sebagai dekorasi rumah atau sebagai hadiah untuk orang tersayang. Saat membeli Batik Mega Mendung, pastikan Anda memilih batik yang asli dan berkualitas. Perhatikan detail motif, warna, dan kain untuk memastikan keaslian batik.\n\nBatik Jawa Barat motif Mega Mendung bukan hanya sebuah kain batik yang indah, tetapi juga merupakan warisan budaya Cirebon yang kaya makna dan filosofi. Batik ini tidak hanya memiliki nilai estetika, tetapi juga memiliki makna spiritual dan budaya yang mendalam. Dengan membeli dan menggunakan Batik Jawa Barat motif Mega Mendung, Anda turut mendukung para pengrajin batik lokal, membantu dalam melestarikan budaya Cirebon, dan membawa keindahan alam dan makna filosofisnya di masa depan.',

    'Batik Jawa Timur motif Pring merupakan bagian dari kekayaan budaya Jawa Timur, Indonesia. Motif ini telah menjadi bagian penting dari warisan budaya daerah tersebut dan terkait erat dengan perkembangan seni batik di Jawa Timur. Motif Pring sering digunakan dalam batik Jawa Timur sebagai simbol kehidupan dan kesejahteraan.\n\nProses pembuatan Batik Jawa Timur motif Pring mengikuti teknik tradisional membatik. Kain katun dipersiapkan untuk dicelupkan ke dalam larutan pewarna. Motif Pring kemudian diaplikasikan pada kain menggunakan teknik canting atau cap untuk menciptakan pola daun yang khas. Setelah proses pewarnaan selesai, kain dicuci untuk menghilangkan lilin dan pewarnaan berlebih, sehingga motif Pring tampak jelas dan indah.\n\nBatik Jawa Timur motif Pring memiliki makna dan filosofi yang mendalam. Daun Pring dianggap sebagai simbol kehidupan dan kelestarian alam. Dalam budaya Jawa, daun Pring sering dikaitkan dengan kemakmuran, kesuburan, dan perlindungan. Kehadiran motif ini dalam batik dapat diartikan sebagai upaya untuk menghargai dan mempersembahkan keindahan alam serta menyampaikan pesan akan pentingnya menjaga alam dan kelestariannya.\n\nMotif Pring memiliki berbagai variasi, seperti Pring Sedapur, Pring Wulung, dan Pring Ron. Setiap variasi memiliki makna dan filosofi yang sedikit berbeda. Warna yang umum digunakan dalam Batik Jawa Timur motif Pring adalah hijau, biru, dan coklat, melambangkan alam dan kesuburan. Batik ini dibuat dengan teknik tradisional membatik, namun juga dapat dibuat dengan teknik batik kontemporer.\n\nBatik Jawa Timur motif Pring sering digunakan dalam berbagai acara adat dan budaya Jawa Timur, seperti pernikahan, festival, dan pertunjukan seni. Harganya bervariasi tergantung pada jenis motif, bahan kain, dan tingkat kesulitan pembuatannya. Batik Pring handmade dengan motif rumit dapat dijual dengan harga yang cukup tinggi.\n\nBatik Jawa Timur motif Pring bukan hanya sebuah kain batik yang indah, tetapi juga merupakan simbol kehidupan dan kesejahteraan serta ekspresi dari kearifan lokal dan nilai-nilai budaya Jawa Timur. Batik ini tidak hanya memiliki nilai estetika, tetapi juga memiliki makna filosofis yang mendalam. Dengan membeli dan menggunakan Batik Jawa Timur motif Pring, Anda turut mendukung para pengrajin batik lokal, membantu dalam melestarikan budaya Jawa Timur, dan membawa pesan tentang pentingnya menjaga alam dan kelestariannya kepada generasi mendatang.',

    'Batik Kalimantan motif Dayak merupakan bagian dari kekayaan budaya Kalimantan yang kaya dan beragam. Motif-motif yang terinspirasi dari kebudayaan suku Dayak, yang merupakan salah satu suku asli Kalimantan, telah menjadi ikonik dalam batik Kalimantan. Sejarah batik ini mungkin sulit ditelusuri secara spesifik, namun telah menjadi bagian integral dari budaya dan seni Kalimantan.\n\nProses pembuatan Batik Kalimantan motif Dayak mengikuti teknik tradisional pembuatan batik. Kain yang biasanya terbuat dari katun atau sutra disiapkan untuk dicelupkan ke dalam larutan pewarna. Motif-motif Dayak kemudian diaplikasikan pada kain menggunakan teknik canting atau cap untuk menciptakan pola yang unik dan khas. Setelah proses pewarnaan selesai, kain dicuci untuk menghilangkan lilin dan pewarnaan berlebih, sehingga motif Dayak tampak jelas dan indah.\n\nLebih dari sekadar keindahan visual, Batik Kalimantan motif Dayak memiliki makna dan filosofi yang mendalam. Motif-motif yang terinspirasi dari budaya suku Dayak sering menggambarkan simbol-simbol kehidupan, alam, dan spiritualitas. Kehadiran motif-motif ini dalam batik dapat diartikan sebagai upaya untuk mempertahankan dan menghargai warisan budaya suku Dayak, serta menyampaikan pesan tentang keberagaman, kehidupan, dan keindahan alam Kalimantan.\n\nBatik Kalimantan motif Dayak memiliki berbagai variasi yang terinspirasi dari berbagai suku Dayak di Kalimantan, seperti Dayak Iban, Dayak Ngaju, dan Dayak Maanyan. Setiap motif memiliki makna dan filosofi yang khas dari masing-masing suku. Warna yang sering digunakan dalam Batik Kalimantan motif Dayak adalah warna-warna cerah dan berani, seperti merah, kuning, dan biru. Warna-warna ini melambangkan semangat, kekuatan, dan keindahan alam Kalimantan.\n\nBatik Kalimantan motif Dayak sering digunakan dalam berbagai acara adat dan budaya suku Dayak, seperti pernikahan, festival, dan pertunjukan seni. Batik ini juga populer sebagai souvenir dan cinderamata khas Kalimantan.\n\nBatik Dayak bukan sekadar kain yang indah, tetapi jendela budaya suku Dayak dan pesona Kalimantan. Batik ini bukan hanya memanjakan mata, tetapi sarat makna filosofis dan budaya. Membeli dan menggunakan Batik Dayak berarti mendukung pengrajin lokal, melestarikan budaya suku Dayak dan Kalimantan, serta menyebarkan pesan tentang keberagaman dan keindahan alam Kalimantan kepada generasi mendatang. Batik Dayak cocok untuk berbagai acara, formal maupun kasual, dan dapat menghiasi rumah atau menjadi hadiah istimewa.',

    'Batik Madura motif Mataketeran memiliki akar yang dalam dalam kehidupan masyarakat Madura. Sejarahnya mungkin sulit ditelusuri secara spesifik, tetapi batik ini telah menjadi bagian penting dari warisan budaya Madura yang diwariskan dari generasi ke generasi. Motif Mataketeran sering kali menjadi simbol identitas dan kebanggaan bagi masyarakat Madura.\n\nProses pembuatan Batik Madura motif Mataketeran mengikuti teknik tradisional pembuatan batik. Kain yang biasanya terbuat dari katun atau sutra disiapkan untuk dicelupkan ke dalam larutan pewarna. Motif Mataketeran kemudian diaplikasikan pada kain menggunakan teknik canting atau cap untuk menciptakan pola yang khas. Setelah proses pewarnaan selesai, kain dicuci untuk menghilangkan lilin dan pewarnaan berlebih, sehingga motif Mataketeran tampak jelas dan indah.\n\nBatik Madura motif Mataketeran mengandung makna dan filosofi yang mendalam. Motif Mataketeran sering kali menggambarkan simbol-simbol kehidupan sehari-hari, tradisi, dan kepercayaan masyarakat Madura. Kehadirannya dalam batik dapat diartikan sebagai cara untuk memperingati dan mempersembahkan kekayaan budaya dan warisan nenek moyang. Batik Mataketeran sering digunakan dalam berbagai acara adat dan budaya Madura, seperti pernikahan, festival, dan pertunjukan seni. Batik ini juga populer sebagai souvenir dan cinderamata khas Madura.\n\nLebih dari sekadar kain batik yang memikat, Batik Madura motif Mataketeran adalah perwujudan identitas dan kebanggaan budaya Madura. Batik ini bukan hanya memanjakan mata, tetapi menyimpan makna filosofis dan nilai budaya yang mendalam. Membeli dan mengenakan Batik Mataketeran bukan hanya soal fashion, tetapi merupakan bentuk dukungan terhadap para pengrajin lokal, upaya melestarikan budaya Madura, dan penyebaran pesan tentang kekayaan budaya Madura kepada generasi penerus. Batik Mataketeran mewarnai berbagai momen, dari acara formal hingga kasual, dan dapat mempercantik rumah atau menjadi hadiah istimewa bagi orang terkasih.',

    'Batik Maluku Pala adalah salah satu varian batik yang berasal dari wilayah Maluku, Indonesia. Batik ini terkenal dengan motif khasnya yang terinspirasi dari buah pala, salah satu komoditas utama dan simbol kebanggaan Maluku. Buah pala tidak hanya penting secara ekonomi bagi Maluku, tetapi juga memiliki nilai historis dan budaya yang mendalam.\n\nMotif batik Maluku Pala biasanya menampilkan gambar buah pala, bunga pala, dan daun pala yang digabungkan dengan unsur-unsur alam lainnya seperti burung, ombak laut, dan tanaman lokal. Desain ini mencerminkan kekayaan alam dan keanekaragaman hayati Maluku serta kehidupan sehari-hari masyarakatnya yang erat kaitannya dengan alam.\n\nBatik Maluku Pala sering menggunakan warna-warna cerah dan natural, seperti hijau, cokelat, merah, dan kuning, yang mencerminkan kesuburan tanah dan keindahan alam Maluku. Proses pembuatannya melibatkan teknik batik tulis dan cap, yang menunjukkan keterampilan dan keahlian tangan para pembatik lokal. Penggunaan pewarna alami juga umum ditemukan dalam pembuatan batik ini, menjaga tradisi sekaligus mendukung keberlanjutan lingkungan.\n\nBatik Maluku Pala bukan hanya sebuah produk tekstil, tetapi juga sebuah simbol identitas budaya. Ia mencerminkan sejarah panjang perdagangan rempah-rempah dan peran penting Maluku dalam jalur perdagangan dunia. Selain itu, batik ini juga berfungsi sebagai sumber pendapatan bagi masyarakat setempat, mendukung industri kerajinan dan pariwisata di wilayah Maluku.\n\nBatik Maluku Pala dapat ditemukan dalam berbagai bentuk pakaian, seperti kain panjang, kemeja, gaun, dan aksesori lainnya. Keunikan motif dan kualitas tinggi dari batik ini membuatnya semakin populer baik di pasar lokal maupun internasional. Banyak perancang busana Indonesia yang mulai mengeksplorasi motif batik Maluku Pala dalam koleksi mereka, sehingga meningkatkan apresiasi dan kesadaran akan warisan budaya Maluku di kalangan yang lebih luas.\n\nSecara keseluruhan, batik Maluku Pala merupakan salah satu representasi yang indah dari kekayaan budaya dan alam Indonesia, menggabungkan sejarah, seni, dan kearifan lokal dalam setiap helainya.',

    'Motif batik Asmat adalah motif batik yang berasal dari Papua dan sangat populer. Nama motif ini diambil dari suku Asmat, suku asli yang tinggal di Papua. Motif batik Asmat biasanya menggambarkan motif kesukuan suku Asmat yang pada umumnya ditemukan pada patung kayu. Warna batik Asmat memiliki ciri khas tersendiri, biasanya menggunakan pewarna alami dari tanah terakota yang berwarna merah kecokelat-cokelatan.\n\nProses pembuatan batik Asmat mirip dengan proses pembuatan batik Jawa, yaitu menggunakan metode tulis atau cap. Proses pembuatan batik tulis membutuhkan waktu yang lebih lama, bisa mencapai 2 hingga 3 bulan atau lebih, tergantung pada kerumitan coraknya. Sedangkan batik cap lebih mudah dibuat karena menggunakan bantuan cetakan.\n\nBatik Asmat diproduksi di banyak daerah di Papua, termasuk provinsi Papua Barat. Pusat pembuatannya biasanya berada di sentra-sentra batik, yaitu terletak di Kota Jayapura. Batik Asmat tidak hanya indah, tetapi juga memiliki makna dan filosofi yang mendalam.',

    'Batik Cendrawasih merupakan salah satu motif batik kontemporer yang berkembang di Papua, Indonesia. Meskipun batik bukanlah tradisi asli Papua, namun dalam beberapa dekade terakhir, seni batik telah diadopsi dan dikembangkan oleh seniman lokal dengan mengintegrasikan unsur-unsur budaya Papua yang kaya. Motif Cendrawasih sendiri mulai populer sekitar awal abad ke-21, bertepatan dengan semakin meningkatnya upaya pelestarian budaya Papua di berbagai bidang seni.\n\nMotif Cendrawasih terinspirasi dari burung Cendrawasih, yang dikenal sebagai burung surga dan merupakan ikon fauna Papua. Burung ini terkenal dengan bulunya yang indah dan tarian kawinnya yang memukau. Motif Cendrawasih pada batik Papua menggambarkan keindahan dan keanggunan burung ini, sekaligus mencerminkan keanekaragaman hayati dan kekayaan alam Papua. Pola ini seringkali digabungkan dengan elemen-elemen alam lainnya seperti dedaunan, bunga-bunga khas Papua, dan simbol-simbol adat lokal.\n\nBatik Papua Cendrawasih tidak hanya menonjolkan keindahan estetika tetapi juga mengandung makna filosofis yang mendalam. Burung Cendrawasih dianggap sebagai simbol kebebasan, keindahan, dan keabadian dalam budaya Papua. Dalam tradisi lokal, burung ini sering dikaitkan dengan mitos dan cerita rakyat yang menggambarkan hubungan harmonis antara manusia dan alam. Pembuatan batik dengan motif Cendrawasih melibatkan teknik pewarnaan dan pengerjaan tangan yang rumit, mencerminkan dedikasi dan keterampilan para pengrajin Papua.',

    'Motif batik Tifa berasal dari Papua dan terinspirasi dari alat musik tradisional Papua, yaitu Tifa. Tifa adalah sejenis alat musik perkusi yang terbuat dari kayu berbentuk tabung. Satu sisi instrumen ditutup dengan kulit binatang kering. Suara yang dihasilkan oleh Tifa terdengar lebih ringan dibandingkan dengan drum.\n\nMotif batik ini juga dikenal dengan nama Tifa Honai. Motif ini melambangkan rumah bahagia, yakni rumah yang dipenuhi kebahagiaan. Dalam motif batik Tifa Honai, terdapat gambar Honai sebagai rumah adat Papua yang melambangkan sebuah keluarga, dan Tifa sebagai alat musik khas Papua yang melambangkan kebahagiaan. Kombinasi keduanya menggambarkan tempat untuk berpulang dan berlindung dalam kebersamaan keluarga yang bahagia.\n\nProses pembuatan batik ini dapat memakan waktu dari satu bulan hingga 2 tahun, tergantung pada kompleksitas prosesnya. Proses memproduksi satu tekstil terdiri dari 8 langkah, mulai dari pembuatan pola lilin pada kain, hingga mengunci warna dengan larutan alami, dan pengeringan. Alat khusus yang disebut Canting digunakan untuk menorehkan lelehan lilin panas pada kain.',

    'Batik Parang adalah salah satu motif batik tertua di Indonesia yang berasal dari keraton-keraton di Solo (Surakarta). Pola ini diyakini sudah ada sejak abad ke-16 pada masa Kerajaan Mataram. Kata "Parang" berasal dari kata "pereng" yang berarti lereng, mencerminkan motif diagonal yang menyerupai ombak atau pedang. Awalnya, motif ini hanya diperuntukkan bagi kalangan bangsawan dan keluarga kerajaan sebagai simbol kekuasaan dan keberanian.\n\nMotif Parang terdiri dari pola berbentuk S yang berulang, melambangkan kekuatan, keteguhan, dan kesinambungan. Pola ini sering diinterpretasikan sebagai ombak laut yang tidak pernah berhenti, mencerminkan semangat pantang menyerah. Ada beberapa jenis motif Parang, seperti Parang Rusak yang melambangkan perjuangan, Parang Barong yang menunjukkan kewibawaan pemimpin, dan Parang Klitik yang melambangkan kelembutan dan kecantikan.\n\nBatik Parang bukan hanya sekedar kain dengan motif indah, tetapi juga sebuah warisan budaya yang kaya akan makna dan sejarah. Hingga hari ini, batik dengan motif Parang sering digunakan dalam upacara adat dan acara penting sebagai penghormatan terhadap tradisi dan warisan leluhur. Dengan memahami cerita di balik motif Parang, kita tidak hanya menghargai keindahan seni batik, tetapi juga merenungkan filosofi dan nilai-nilai yang diwariskan oleh nenek moyang kita.',

    'Batik Lontara, sebuah warisan budaya yang berasal dari Sulawesi Selatan, memikat mata dengan coraknya yang unik dan penuh makna. Batik ini tidak hanya indah dipandang, tetapi juga menyimpan cerita panjang tentang sejarah, tradisi, dan filosofi masyarakat Bugis-Makassar.\n\nBatik Lontara lahir dari tangan kreatif Aisyahrani, seorang seniman asal Makassar di tahun 2008. Beliau terinspirasi oleh kekayaan budaya Bugis-Makassar yang terukir dalam Aksara Lontara, sebuah sistem aksara tradisional yang telah ada sejak abad ke-9. Aisyahrani ingin melestarikan warisan budaya ini dengan menuangkannya ke dalam bentuk seni batik.\n\nKeunikan Batik Lontara terletak pada motifnya yang terinspirasi dari Aksara Lontara. Motif-motif ini tidak hanya indah, tetapi juga memiliki makna filosofis yang mendalam. Contohnya, motif Kalimata yang melambangkan keseimbangan dan keselarasan hidup, motif Ular yang melambangkan kekuatan dan kewaspadaan, dan motif Perahu yang melambangkan semangat pantang menyerah.\n\nBatik Lontara bukan sekadar kain bermotif indah, tetapi juga sebuah identitas budaya Sulawesi Selatan. Batik ini menjadi simbol pelestarian budaya dan tradisi masyarakat Bugis-Makassar. Bagi pemakainya, Batik Lontara menjadi wujud rasa cinta dan penghargaan terhadap warisan leluhur.\n\nLebih dari itu, Batik Lontara juga memiliki nilai ekonomi yang tinggi. Batik ini telah menjadi salah satu produk unggulan Sulawesi Selatan dan diminati oleh wisatawan lokal maupun mancanegara. Kehadiran Batik Lontara telah membuka lapangan pekerjaan bagi masyarakat dan membantu meningkatkan perekonomian lokal.',

    'Batik Boraspati merupakan salah satu motif batik khas Sulawesi Utara yang sarat akan sejarah, asal-usul, dan cerita yang menarik. Berasal dari Minahasa, batik ini telah menjadi bagian integral dari budaya dan tradisi masyarakat setempat selama berabad-abad.\n\nAsal-usul batik Boraspati dapat ditelusuri kembali ke masa penjajahan Belanda. Saat itu, para bangsawan Minahasa sering berinteraksi dengan para pejabat Belanda yang mengenakan batik. Terinspirasi oleh keindahan dan keanggunan batik, para pengrajin Minahasa mulai menciptakan batik mereka sendiri dengan motif dan makna yang mencerminkan budaya mereka.\n\nNama Boraspati sendiri berasal dari kata Bora yang berarti hari Kamis dan Spati yang berarti penguasa. Motif batik ini biasanya dikenakan pada hari Kamis, hari yang dianggap suci dalam kepercayaan Minahasa.\n\nBatik Boraspati terkenal dengan motifnya yang rumit dan penuh makna. Motif utama biasanya berupa gambar hewan, seperti burung, naga, dan kuda laut, yang melambangkan kekuatan, keberanian, dan kemakmuran. Motif lain seperti bunga dan daun melambangkan keindahan alam dan kesuburan.\n\nBatik Boraspati bukan hanya sebuah kain yang indah, tetapi juga merupakan warisan budaya yang berharga bagi masyarakat Minahasa. Batik ini terus dilestarikan dan diwariskan dari generasi ke generasi, membawa serta cerita dan makna yang telah diwariskan sejak zaman dahulu.\n\nBatik Boraspati tidak hanya digunakan dalam acara-acara adat dan keagamaan, tetapi juga telah menjadi bagian dari fashion modern. Saat ini, banyak desainer yang menggabungkan motif batik Boraspati dengan desain modern, menciptakan karya seni yang unik dan penuh makna.\n\nBatik Boraspati adalah contoh nyata bagaimana budaya dan tradisi dapat dihidupkan kembali melalui seni dan kreativitas. Batik ini tidak hanya menjadi kebanggaan masyarakat Minahasa, tetapi juga menjadi bagian dari kekayaan budaya Indonesia yang patut dilestarikan.',

    'Batik Kawung adalah salah satu motif batik klasik yang berasal dari Kesultanan Yogyakarta. Motif ini sudah ada sejak abad ke-13 dan sering kali dikaitkan dengan era Kerajaan Mataram Kuno. Kata "Kawung" sendiri merujuk pada buah kolang-kaling (buah aren), yang bentuknya menyerupai pola pada batik ini. Pada awalnya, motif Kawung hanya boleh dikenakan oleh keluarga kerajaan sebagai simbol kebijaksanaan dan keadilan.\n\nMotif Kawung memiliki akar yang dalam dalam budaya Jawa. Legenda menyebutkan bahwa motif ini diciptakan oleh Sunan Kalijaga, salah satu Wali Songo yang berperan penting dalam penyebaran Islam di Jawa. Motif Kawung terdiri dari pola geometris berupa lingkaran-lingkaran yang tersusun rapi dan simetris. Pola ini melambangkan keseimbangan dan kesucian. Selain itu, ada kepercayaan bahwa motif ini juga terinspirasi dari bentuk bunga teratai yang dianggap suci dan melambangkan keabadian.\n\nBatik Kawung memiliki makna filosofi yang mendalam. Pola lingkaran yang berulang menggambarkan harmoni dan keselarasan hidup. Ada beberapa variasi motif Kawung, seperti Kawung Picis, Kawung Bribil, dan Kawung Sen, yang masing-masing memiliki ukuran dan penyusunan yang berbeda. Kawung Picis, misalnya, memiliki lingkaran-lingkaran kecil yang rapat, sementara Kawung Bribil memiliki lingkaran yang lebih besar dan jarang. Dalam budaya Jawa, penggunaan batik Kawung pada pakaian menunjukkan sifat rendah hati dan introspektif, mengingatkan pemakainya untuk selalu merenungkan perbuatannya.'
]

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure request is POST
    if request.method == 'POST':
        # Ensure there is a file part in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        
        # Ensure the file is not empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Ensure the file is an image
        if file and allowed_file(file.filename):
            # Read the image and do preprocessing
            img = Image.open(file)
            img = img.resize((300, 300))  # Resize image
            img_array = np.array(img) / 255.0  # Normalize
            
            # Expand dimensions and add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            # Predict class
            prediction = model.predict(img_array)
            print(prediction)
            predicted_class_index = int(np.argmax(prediction))
            predicted_class_name = class_names[predicted_class_index]
            batik_desc = class_desc[predicted_class_index]
            
            # Provide response with predicted class label
            return jsonify({'class_index': predicted_class_index, 'batikName': predicted_class_name, 'batikDesc': batik_desc})
        else:
            return jsonify({'error': 'Invalid file type'})




if __name__ == '__main__':
    app.run(debug=True)