![Alt text](https://github.com/joe7342/opencvdraw/blob/master/img/cover.png)

## Create a virtual pen and eraser with python and OpenCV
## 使用Python 與 OpenCV 建立虛擬畫筆及橡皮擦

本專題是基於輪廓檢測(contour detection)而創建，在此程式結構中有7項重點：

1. 尋找目標筆的顏色範圍並保存。
2. 應用形態學運算(morphological operations)。
3. 偵測並追蹤有顏色之物體。
4. 找到筆繪製的x,y坐標。
5. 畫面清除功能。
6. 虛擬橡皮擦切換功能。
7. 截圖功能。

重點1~4為虛擬畫筆的建構，先使用顏色遮罩（color masking）來取得手上拿的筆的二元遮罩（binary masks），執行形態學運算以消除雜訊，然後使用輪廓檢測來追蹤該筆在螢幕上的位置。此功能實際上就是將點與點之間連接起來，也就是使用筆畫線的初始位置的（x,y）和筆移動中的（x,y）之間畫一條線，並針對攝影機中的每一幀進行繪製，這樣就可以用筆即時繪製圖形，如此一來我們就有了支虛擬畫筆。

成功建立虛擬畫筆後，再來是增加功能使程式更加完善，一是畫面清除功能，將螢幕上所有的畫線清除，方法就是偵測手上筆與攝影鏡頭的距離，如果距離太近就會清除螢幕回到初始狀態。

現在我們已經完成筆和螢幕清除的部分，最後就是加入切換虛擬橡皮擦的功能，當切換到橡皮擦時即可清除畫筆畫的線，另個部分是筆與橡皮擦之間的轉換，要做的就是將手放在屏幕左上角的圖示時時進行切換，我們使用背景分離技術（background subtraction）來監控圖示區域，當手移動到該區域造成干擾時，就如同按下虛擬切換按鈕一般。最後加上截圖功能，可存下繪圖成果。

今年由於武漢疫情關係，現在全世界不論是工作會議及學校教育等...都非常依賴視訊軟體，此項目希望能讓視訊交流增添更多互動性，甚至往娛樂發展，例如繪畫猜圖遊戲等應用。

***

參考：
+ https://www.learnopencv.com/creating-a-virtual-pen-and-eraser-with-opencv/
+ https://blog.csdn.net/gaoyu1253401563/article/details/85253511
+ https://sites.google.com/a/ms.ttu.edu.tw/cse2012dance-robot/yan-jiu-cheng-guo/opencv-ruan-ti-she-ji/qin-shi-yu-peng-zhang
+ https://makerpro.cc/2018/11/opencv-background-subtractor/
+ https://blog.csdn.net/m0_37901643/article/details/72841289
+ https://blog.csdn.net/zhangyonggang886/article/details/51638655
+ https://blog.csdn.net/lwplwf/article/details/73551648
+ http://opencv123.blogspot.com/2015/06/
