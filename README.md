# Volleyball_Text_Labelling

載入影片後，先分成兩大類：得分/失分

- 得分 (score)
    - 組織進攻得分 (strategy)
    - 發球進攻得分 (serving)
- 失分 (lose)
    - 遭對方攔網失分 (blocking)
    - 發球失誤 (serving error)
    - 傳球失誤 (pass mistake)
    - 攻擊失誤 (attack error)

---

每個影片用最多三句話來描述，分別是一傳、二傳、進攻。

這裡可以透過 ON/OFF 來決定每一句話是否要加入到描述句子中。

以下為各狀態下的公式句，這裡只要協助加入下拉式選單的部分(粗體字)，最後按下左下方 save text 即完成該影片的標註


- 得分 (score)
    - 組織進攻得分 (strategy)
        1. The  **(Setter1)** receives the ball at **(position W)** and passes the ball to  **(positon X)** .
        2. the **(Setter2)** at **(positon X)** sets the ball to **(positon Y)**, 
        3. and the **(ATTACKER)** at **(positon Z)** gets a point by **(ATTACK_METHOD)**.
    - 發球進攻得分 (serving)
        1. The server serves the ball to the opponent’s  **(position X)** , and the oppoent dig outside.

- 失分 (lose)
    - 遭對方攔網失分 (blocking)
        1. The  **(Setter1)** receives the ball at **(position W)** and passes the ball to  **(positon X)** .
        2. the **(Setter2)** at **(positon X)** sets the ball to **(positon Y)**, 
        3. and the **(ATTACKER)** at **(positon Z)** is blocked, leading to a point for the opposing team on a **(ATTACK_METHOD)** attack.
    - 發球失誤 (serving error)
        1. The server loses a point due to a serving error.
    - 傳球失誤 (pass mistake)
        1. The  **(Setter1)** receives the ball at **(position W)** and passes the ball to  **(positon X)** .
        2. the **(Setter2)** at **(positon X)** sets the ball to **(positon Y)**, 
        3. and loses a point due to a passing mistake.
    - 攻擊失誤 (attack error)
        1. The  **(Setter1)** receives the ball at **(position W)** and passes the ball to  **(positon X)** .
        2. the **(Setter2)** at **(positon X)** sets the ball to **(positon Y)**, 
        3. and the **(ATTACKER)** at **(positon Z)** loses a point due to an attack error while executing a **(ATTACK_METHOD)** attack.