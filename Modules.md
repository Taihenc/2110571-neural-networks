### 🧠 Module 1: The Engine (MLP, Backpropagation & Optimization)

*จุดที่อาจารย์มักจะออกข้อสอบคำนวณมือ (Manual Optimization) ลากไส้สมการ*

#### 1. Forward Pass & Activation Functions

* **Forward Pass (Initial Output):**
* **คืออะไร:** การยิง Input เข้าไปคูณกับ Weight บวก Bias แล้วผ่าน Activation Function เพื่อดูว่าโมเดล "เดา" คำตอบแรกได้อะไร
* **สมการ:** $z = \sum (w_i \cdot x_i) + b$ และ Output $a = f(z)$


* **Activation Functions:** (ตัวดัดกราฟให้โค้งงอ เพื่อแก้ปัญหาที่ซับซ้อน)
* **Sigmoid:** บีบค่าเป็นช่วง $[0, 1]$ (ใช้บอกความน่าจะเป็น) ข้อเสียคือเกิด Vanishing Gradient ได้ง่าย (Gradient ใกล้ศูนย์)
* **Hyperbolic Tangent (Tanh):** บีบค่าเป็นช่วง $[-1, 1]$ **(Zero-centered)** ทำให้ Convergence (การลู่เข้าหาคำตอบ) เร็วกว่า Sigmoid


* **🚨 Exam Hack & Pitfalls:**
* **ข้อสอบ Choice มักถาม:** "ทำไม Tanh ถึงดีกว่า Sigmoid ใน Hidden Layer?" **ตอบ:** เพราะ Tanh มีค่าเฉลี่ยอยู่ที่ 0 (Zero-centered) ทำให้ทิศทางการอัปเดต Weight ใน Backprop ไม่เหวี่ยงไปทางบวกหรือลบเพียงทิศทางเดียว (แก้ปัญหา Zig-zag convergence)
* **Forgetting Bias Weight ($W_0$):** จุดตายเบอร์ 1 ตอนคำนวณมือ! อย่าลืมว่า Bias คือ Node ที่มีค่า Input เป็น 1 เสมอ ($x_0 = 1$)



#### 2. Loss & Optimization

* **Cross Entropy vs. MSE:**
* **MSE (Mean Squared Error):** เหมาะกับงาน Regression (ทายตัวเลข) กราฟ Loss จะเป็นรูปกระทะ (Convex)
* **Cross Entropy:** เหมาะกับ Classification (ทายหมวดหมู่) **ข้อสอบมักถามว่าทำไมไม่ใช้ MSE ทายหมวดหมู่?** ตอบ: เพราะถ้าใช้ MSE + Sigmoid/Softmax กราฟมันจะไม่ใช่ Convex ทำให้ Optimization ไปติดหล่ม (Local Minimum) ได้ง่าย


* **Softmax for Multi-class:** แปลงค่าผลลัพธ์ (Logits) ให้กลายเป็นความน่าจะเป็นที่รวมกันได้ 1 สูตรคือ $\frac{e^{x_i}}{\sum e^{x_j}}$
* **Gradient Descent (Batch vs. Stochastic):**
* *Batch:* ดู Data ทั้งหมดค่อยอัปเดต Weight ทีเดียว (เสถียรแต่ช้า)
* *Stochastic (SGD):* สุ่ม Data มา 1 ตัวแล้วอัปเดตเลย (แกว่ง เร็ว แต่มีโอกาสหลุดจาก Local Minimum ได้ดีกว่า)



#### 3. Backpropagation (The Hardcore Math)

* **คืออะไร:** กฎลูกโซ่ (Chain Rule) เพื่อหาว่าโหนดไหน/เส้นไหน มีส่วนทำให้เกิด Error เท่าไหร่ จะได้ปรับ Weight ได้ถูก
* **Output Node Delta Calculation ($\delta_k$):** คำนวณ Error ที่ปลายทาง สูตรทั่วไปคือ $(Target - Output) \cdot f'(z)$
* **Hidden Node Delta Calculation ($\delta_j$):** เอา Delta ของโหนดปลายทาง มาคูณกับ Weight ที่เชื่อมอยู่ แล้วคูณกับ Derivative (ดิฟ) ของโหนดปัจจุบัน
* **Weight Updating Strategy:** $w_{new} = w_{old} + (\eta \cdot \delta \cdot input)$ ($\eta$ คือ Learning Rate)
* **🚨 ทริคคำนวณมือ (Sequential/Cascading Errors):** ถ้าอาจารย์ให้คำนวณ 2 Epochs **ตั้งสติให้ดี!** ถ้าคุณคิด Delta ของ Layer สุดท้ายผิด มันจะลาม (Cascade) ทำให้ Hidden Layer ผิดตามไปเป็นโดมิโน่ เช็คเครื่องหมาย $+$ $-$ ให้ขาด

---

### ⚔️ Module 2: Support Vector Machines (SVM)

*การสร้างพรมแดนที่ปลอดภัยที่สุด*

* **Widest Margin Boundary & Identify Support Vectors:**
* SVM พยายามสร้าง "ถนน" (Margin) กั้นระหว่าง 2 คลาสให้กว้างที่สุด
* **Support Vectors:** คือ Data points ที่ "เหยียบเส้นขอบถนน" พอดี ข้อมูลตัวอื่นที่อยู่ห่างออกไปจะ**ไม่มีผลใดๆ ต่อการสร้างสมการเส้นแบ่งเลย** (ทริค: ค่า Lagrange Multipliers $\alpha$ ของจุดที่ไม่ใช่ Support Vector จะมีค่าเป็น 0 เสมอ!)


* **Determine Final Weight Vector ($w$):** คำนวณจาก $w = \sum (\alpha_i \cdot y_i \cdot x_i)$
* **Space Transformation & Non-linearly Separable Data:**
* ถ้าข้อมูลมันกอดกันกลม แบ่งด้วยเส้นตรงไม่ได้ (เช่น วงกลมซ้อนวงกลม) จะทำยังไง?
* **Exam Hack:** ใช้สิ่งที่เรียกว่า **"Kernel Trick"** (เช่น RBF Kernel) โยนข้อมูลพุ่งขึ้นไปในมิติที่ 3 (High-dimensional space) แล้วใช้ "แผ่นระนาบ" (Hyperplane) ฟันฉับแบ่งข้อมูลได้อย่างสวยงาม



---

### 👁️ Module 3: Convolutional Neural Networks (CNN)

*สถาปัตยกรรมการมองเห็นของ AI*

* **Layer Mechanics & Feature Map Generation:**
* หลักการคือใช้ **Kernel Filters (เช่น 3x3 หรือ 5x5)** เลื่อนทาบ (Slide) ไปบนภาพตามสเตปก้าวที่เรียกว่า **Stride** เพื่อดึง Pattern (ขอบเส้น, สี, รูปทรง) ออกมาเป็น **Feature Map**


* **2x2 Max Pooling:** คือการ Downsampling ยุบขนาดภาพให้เล็กลงโดยเลือก "ค่ามากสุด" ในกรอบ 2x2 มาเป็นตัวแทน (ช่วยลดภาระการคำนวณและป้องกัน Overfitting)
* **🚨 ทริคข้อสอบ:** Pooling Layer **ไม่มี Parameter** ให้เรียนรู้ (Weights = 0) ถ้าอาจารย์ให้คำนวณจำนวน Parameter ใน CNN ข้าม Pooling ไปได้เลย!


* **Architectures (LeNet & ResNet50):**
* *LeNet:* คุณปู่ของ CNN มีโครงสร้างเรียบง่าย Conv -> Pool -> FC Layers
* *ResNet50 / Pre-trained Models:* ลึก 50 ชั้น ข้อสอบชอบถามว่า "โมเดลลึกๆ แก้ปัญหา Vanishing Gradient อย่างไร?" คำตอบคือ ResNet มีวงจร **Skip Connection (Shortcut)** ให้ Gradient ไหลข้าม Layer ได้



---

### 🕵️ Module 4: Unsupervised Learning

*ให้ AI จัดกลุ่มเองโดยไม่มีเฉลย (Labels)*

* **K-Means Clustering:**
* 1. สุ่มจุดศูนย์กลาง (**Centroid Calculation**)


* 2. วัดระยะทางของทุกจุดหา Centroid ที่ใกล้สุด (**Distance Measurement** มักใช้ Euclidean Distance)


* 3. จัดกลุ่มเสร็จ ก็หาค่าเฉลี่ยของกลุ่มใหม่ ย้าย Centroid ไปตรงกลางกลุ่ม (**Iterative Mean Updating**) แล้วทำซ้ำจนกว่าจะไม่ขยับ




* **Self-Organizing Maps (SOM):**
* ใช้ **Kohonen Layer** (1 Layer กางเป็นตาข่าย 2 มิติ)
* Data เข้ามา Node ทุกตัวจะแข่งกัน ตัวที่ชิงความคล้ายคลึงได้มากสุดคือ **Winning Neuron**
* **Lesser ID Tie-break:** ทริคเฉพาะ ถ้าแข่งแล้วมีตัวชนะ 2 ตัวเสมอ กติกาบังคับให้เลือก Node ที่ ID (หมายเลข) น้อยกว่าเป็นผู้ชนะ
* จากนั้นอัปเดต Weight ของผู้ชนะและ "เพื่อนบ้าน" (Neighborhood) ให้หน้าตาเหมือน Data point นั้นมากขึ้น (**Neighborhood Weight Updates**)



---

### 📜 Module 5: Sequential Models & NLP

*สถาปัตยกรรมสำหรับข้อมูลที่มี "ลำดับเวลา" (Time-Series & Language)*

* **LSTM (Long Short-Term Memory):**
* เกิดมาแก้ปัญหาที่ RNN ความจำสั้น ลืมข้อมูลต้นประโยค
* **Cell States (Memory Highway):** เป็นสายพานลำเลียงความจำระยะยาว วิ่งทะลุจากซ้ายไปขวาโดยไม่โดนรบกวนมากนัก
* **Forget Gate (Sigmoid):** ตัดสินใจว่า "ขยะเก่าๆ" ไหนควรทิ้ง (ถ้าผลออกใกล้ 0 คือโยนทิ้ง)
* **Input/Output Gates:** ควบคุมการรับข้อมูลใหม่และการคายข้อมูลออกไปใช้


* **Natural Language Processing (NLP):**
* **Word2Vec Embedding:** แปลง "คำ" ให้กลายเป็นพิกัดตัวเลขในอวกาศความหมาย (Vector Space) ทำให้บวก/ลบคำได้ เช่น $King - Man + Woman = Queen$
* **Transformers (High-level):** สถาปัตยกรรมระดับเทพที่ใช้กลไก **Self-Attention** คือแทนที่จะอ่านทีละคำแบบ LSTM มันจะกางประโยคพรึบ! แล้วมองหาความเกี่ยวโยงของทุกคำพร้อมๆ กัน (นี่คือหัวใจของเทคโนโลยีการสร้าง AI Agent หรือ RAG ขั้นเทพในปัจจุบัน)