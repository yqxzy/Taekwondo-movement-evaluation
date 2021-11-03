# Taekwondo movement evaluation
 ## **An Evaluation of Taekwondo Movements Based on Computer Vision**

> Prepared by: 马成棋，王则宇，Ooi Yee Jing



**Abstract:** We hope to use the depth camera to extract the skeleton data of the taekwondo tester and the skeleton data of the taekwondo teacher (standard action data), compare them and get the similarity between them to score.



<u>**1. Introduction**</u>

**1.1** **Background**

​		The structure of Taekwondo test has a simplified model and required a high standardization. At present, manual testing is mainly adopted in the Taekwondo test. However, manual testing has some limitations such as the contingency in the evaluation and the lower efficiency due to the huge requirement of man power, which result in a waste of human resources and also the high examination fees. Therefore, computer testing had been proposed to use in the Taekwondo test to improve the efficiency, reduce the cost and investments of resources, as well as conducive to the fairness of the Taekwondo test.



**1.2** **Application scenarios**

​		This evaluation system of Taekwondo movements is suitable to use in Taekwondo test or daily training which can assist teachers to guide or evaluate the posture of students.



**1.3 Professional guidance in taekwondo**

​		赵洋, an outstanding party member who takes part in Taekwondo sport events was graduated from Special Operation College of PLA with a master degree and she is a national referee for both Taekwondo and Karate events. Since the year of 2000, she has been engaged in Taekwondo training and teaching for about 21 years. Besides, she was the 49kg main athlete in the national team who had been participated in many national and international competition on behalf of China University Students, GuangDong Province as well as the country, and had successfully won a lot of championships. Furthermore during her teaching period, a lot of students were trained to win the champion in the Taekwondo National Competition and also the first prize in University Technique Competition. She has rich practical teaching experiences and also solid teaching theories.



<u>**2. Description of Work**</u>

**2.1 Data Collection**

**2.1.1 Equipment : Kinect 2.0**

* **Basic parameters:**
  * RGB: 1920 x 1080@30/15 FPS (based on ambient brightness)
  * Depth: 512 x 424@ 30 FPS, 16bit range (mm), detection range of 0.5-4.5 M
  * Infrared camera: 512 x 484,30 Hz
  * FOV: 70 ° to 60 ° x
  * Depth identification range: 0.5 -- 4.5 meters
  * 1080p color camera 30 Hz (15 Hz under low light conditions)

* **Advantages:**

  *  The camera uses TOF to get the depth data, which accuracy is higher than Kinect 1.0.

  * Kinect 2.0 can extract 25 skeleton nodes and bone nodes would not jump easily as shown in Diagram 2.1.1.

    <center>Diagram 2.1.1 Skeleton Tracking Diagram for Kinect 2.0</center>             
    
<u>**3. Difficulty of Work**</u>


**3.1 Measurement of Strength**

**2021.10.27**
​		 Taekwondo techniques always required a large amount of muscular strength to done the Taekwondo movements such as the kicks and hand strikes, the strength of movements is also one of the important parts of evaluation during Taekwondo test. However, the measurement of strength might be hard to achieve by only using the depth camera. Depth camera is suitable and accurate to evaluate the correctness of the postures by measuring the angle, however the strength can only be evaluated depends on the speed of the movements which is inaccurate.    



<u>**4. Progress of Work**</u>

**2021.10.27**
​		 At present, we have completed data collection and processing, and implemented the evaluation part of the code, but we have not conducted debugging, so we have not determined the specific parameters in the code, but we have a relatively complete implementation idea. In the following part, we will process the obtained data more exactly, and collect the standard data with the help of the Taekwondo instructor and extract its characteristic values. Then, according to the comparison result distribution of the two groups of skeleton data, some scoring rules are formulated.



