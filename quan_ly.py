import { GoogleGenerativeAI } from "@google/generative-ai";

// 1. Cấu hình API Key (Lưu trong biến môi trường của Vercel)
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

async function phanTichCalo(fileAnh) {
    // 2. Chuyển đổi file ảnh từ Camera thành định dạng base64 để gửi đi
    const imageData = await fileToGenerativePart(fileAnh, fileAnh.type);
    
    // 3. Gọi AI
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
    const prompt = "Hãy nhận diện món ăn này, liệt kê thành phần và tính Calo...";
    
    try {
        const result = await model.generateContent([prompt, imageData]);
        const response = await result.response;
        console.log(response.text()); // In kết quả ra màn hình web
    } catch (error) {
        console.error("Lỗi AI:", error);
    }
}
