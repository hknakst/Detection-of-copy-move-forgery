# Detection-of-copy-move-forgery

![algorithm](https://github.com/hknakst/Detection-of-copy-move-forgery/blob/master/photos/algorithm.png)

**The objective of the project**: In this Project, it is aimed to determine the frauds that can be made by copying a certain area within an image and pasting it to the same image. Also this project is intended to be resistant to algorithms that compress an image, such as jpeg.



## Türkçe dökümanı (Turkish document)
**Projenin hedefi**: Bu Projede bir görüntünün içerisinde yer alan belirli bir alanın
kopyalanarak, yine aynı görüntüye yapıştırılmasıyla yapılabilecek sahteciliklerin tesbit
edilmesi hedeflenmektedir.Yine bu projenin, jpeg gibi bir görüntüyü sıkıştıran
algoritmalara karşı dayanıklı olması hedeflenmiştir.

**Projenin uygulaması**: Projenin algoritması(uygulaması) Şekil 1’de görülmektedir. Biz
projemizde görüntüyü 8’erlik (8x8) bloklara ayırmayı tercih ettik bunun sebebi daha
küçük alanlardaki sahtecilikleri tesbit etmeyi mümkün kılmak(16’lık bloklar da
gürültüyü azaltmak için tercih edilebilir.).

Bu projede sıkıştırılmalara karşı dayanıklı olması adına bloklara DCT
uyguladık daha sonra DCT ‘nin sonucuna zigzag tarama yapılarak alçak frekans
bölgesini çıkardık. Bunun amacı görüntüdeki anlamlı yani alçak frekanslı bölümü elde
etmek, zigzag tarama sonrası 1x64 lük bir vektör elde ediyoruz bu vektörün ilk
16(alcak frekans kısmı)elemanını alarak gerisiyle ilgilenmedik, çıkarılan bu bölüm
quantalama matrisine veya belirlenen bir sabite(16gibi) bölünür biz bu projede ikisinide
zaman zaman uyguladık, böylece algoritmamız sıkıştırılmalara dayanıklı hale geldi.

Tüm bloklara bu işlemler uygulandıktan sonra her bloğu temsil eden vektörler
alt alta sıralanır ve bir matris elde etmiş oluruz bu matrisin boyutu
“16xblocksayısı”dır.Vektörleri karşılaştırma maliyetini azaltmak için bu matrisi
sütunları baz alınarak, sözlük sıralamasına göre yeniden sıraladık. Böylece benzer
vektörleri birbirine yakın hale getirmiş olduk ayrıca hangi vektörün hangi bloğu temsil
ettiğini kaybetmemek için 1x16lık vektörlerin sonuna blokların başlangıç
koordinatlarını da ekleyerek 1x18’lik hale getirdik ama sıralma yaparken bu sütunları
hesaba katmıyoruz.


Sıralanan vektörlerin benzerliklerini incelemek için sırasıyla belirlenen
vektörün yine belirlenen sayıda komşu vektörleriyle öklid’i hesaplanır.Hesaplanan bu
değer 0’a nekadar yakınsa iki vektör okadar benzerdir anlamına gelir bu projede öklid
eşiği olarak 3.5 , bir vektörün kaç komşusu ile kıyaslanacağı da 8 olarak seçilmiştir.
Öklid eşiği 3.5 çok büyük bir sayı olsada sonraki aşamada doğrultuluklarına göre eleme
işlemi yapılacağı için biraz büyük bir değer seçilmesinin daha iyi sonuçlar verdiğini
gördük.

Benzerlik(öklid) eşiğini geçen vektörler bu sefer de uzaklık eşiği filtresinden
geçer bunun amacı çok yakındaki alanların ilişkilendirilmemesidir.Bu işlemde yine
öklid ile yapılır ama bu sefer vektörler yerine vektörlerin temsil ettiği blokların başlagıç
koordinatları kullanılır. Bu işlemde eğer iki blok arasındaki mesafe yeterince fazla
değilse elenir bu projede minimum iki vektör arasındaki uzaklık 100pixel seçilmiştir.Bu
işlem sonucunda gökyüzü, çöl gibi çok fazla benzer bölge içeren görüntülerde bile iyi
sonuçlar gözlemledik.

Son olarak bu iki eşiği de geçen vektörlerin temsil ettiği blokların başlagıç
koordinatları kullanılarak, iki noktanın mutlak doğrultusunu hesapladık.Hesaplanan bu
doğrultunun, tamemen sıfırlardan oluşan görüntü büyüklüğünde bir uzayda ki
konumunu bulunarak bu konum bir arttırdık.Ayrıca hangi blokların hangi doğrultuyu
arttırdığını kaybetmemek için blokların koordinatlarını ve doğrultularını vektörler
şeklide tutduk.Doğrultuları mutlak hesapladığımız için paralel olmayan konumlar’da
aynı doğrultuya sahip olabiliyordu bunun için bu vektörlerde bir de doğrultunun
yönünü tuduk ve daha iyi sonuçlar elde ettik.Bu uzaydaki en büyük değere sahip
konumu tesbit ederek bu sayının %90’ınından büyük olan bölgeleri bulduk,
bu doğrultuya sahip vektörleri yine bu uzaydan elde ettik ve sahteciliği tesbit etmiş olduk.

## sample results (örnek sonuçlar)

![result2](https://github.com/hknakst/Detection-of-copy-move-forgery/blob/master/photos/result2.png)
![result1](https://github.com/hknakst/Detection-of-copy-move-forgery/blob/master/photos/result1.png)
