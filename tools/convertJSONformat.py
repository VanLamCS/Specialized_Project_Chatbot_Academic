import json

# Nhập dữ liệu từ đầu vào
text = """Ngoại ngữ
I. Nộp chứng chỉ ngoại ngữ / Xét miễn:

1. Nộp chứng chỉ ngoại ngữ (CCNN):

- Truy cập myBK (mybk.hcmut.edu.vn) >> Đăng ký nộp Chứng chỉ ngoại ngữ / Xét miễn.

-  Điền thông tin về CCNN đã đạt và kèm theo file chụp hoặc scan CCNN (không cần nộp trực tiếp tại PĐT).

-  Theo dõi kết quả thẩm tra (sau khoảng tối đa 01 tháng).

TOEIC, IELTS, Chứng nhận VNU-EPT và Chứng chỉ VSTEP quốc gia: Phòng Đào tạo (PĐT) tự động lấy dữ liệu thẩm tra nếu Sinh viên (SV) thực hiện đúng theo quy trình (Áp dụng từ 01/12/2022).
TOEFL iBT, KET, PET, FCE, CAE: SV mang một bản sao CCNN đến Trung tâm ngoại ngữ trường Đại học Bách Khoa để được xác nhận và nộp tại Phòng Đào tạo (Áp dụng từ 01/12/2022).
Lưu ý:

SV có thể nộp CCNN vào bất cứ thời điểm nào trong quá trình học. Lưu ý: CCNN phải còn hiệu lực ít nhất 1 tháng tại thời điểm nộp, SV nên nộp ngay khi đạt CCNN, kết quả CCNN này được dùng để xét miễn các môn anh văn (xem Mục 2), xét điều kiện nhận LVTN /KLTN và xét tốt nghiệp (theo Quy định về chuẩn ngoại ngữ ). Khi đã được xác định đạt các chuẩn thì không cần nộp lại để xác định lại, Ví dụ: nếu đã nộp CCNN đạt yêu cầu LVTN /KLTN thì không cần nộp lại đăng ký LVTN /KLTN (dù cho CCNN đã nộp hết hiệu lực).
Sinh viên vui lòng xem Quy chế học vụ đào tạo tại hcmut.edu.vn >> Đào tạo >> Quy chế - quy định >> Quy định về học vụ và đào tạo bậc đại học – Phiên bản hợp nhất/ Phụ lục 7. Quy định về chuẩn ngoại ngữ dành cho chương trình giảng dạy bằng tiếng Việt/ Chuẩn ngoại ngữ từng năm; 2. Chuẩn ngoại ngữ tốt nghiệp; 3. Quy đổi các bằng cấp & CCNN
 2. Xét miễn các môn anh văn 1, 2, 3, 4:

SV đăng ký xét miễn sau khi đã đăng ký nộp Chứng chỉ ngoại ngữ (xem Mục 1).

Sau đó thanh toán lệ phí tại myBK >> BKPay.

- Theo dõi tình trạng xét miễn tại myBK >> Đăng ký nộp Chứng chỉ ngoại ngữ / Xét miễn

- Cập nhật kết quả xét miễn tại Mybk >> Thông tin sinh viên >> Điểm chuyển (Thời gian cập nhật dự kiến sau 1 tháng nếu SV đã hoàn tất thanh toán lệ phí).

Lưu ý:

Nếu kết quả thẩm tra CCNN là không hợp lệ thì kết quả xét miễn các môn anh văn 1, 2, 3, 4 sẽ không được tính vào bảng điểm của SV và không hoàn lại tiền lệ phí xét miễn đã thanh toán. 
Các môn anh văn được xét miễn được ghi điểm miễn vào mục điểm chuyển / bảo lưu trên bảng điểm, SV sẽ nhận điểm miễn các học phần gốc, tính tích lũy tín chỉ, không tính vào điểm trung bình tích lũy.
Từ Khóa 2021 về sau: trong thời hạn không quá 01 năm, có thể dùng CCNN còn thời hạn phù hợp để được xét miễn các môn Anh văn 1, 2, 3, 4. Riêng SV khóa 2021 được đặc cách gia hạn đến hết Học kỳ 222. Nên SV khóa 2021, khóa 2022 hạn cuối nộp CCNN để đăng ký xét miễn và phải hoàn tất thanh toán lệ phí xét miễn đến hết ngày 30/09/2023. Sinh viên khóa 2023 hạn cuối nộp CCNN để đăng ký xét miễn và phải hoàn tất thanh toán lệ phí xét miễn đến hết ngày 08/09/2024
Quy định mới áp dụng bắt đầu từ Học kỳ 222: Chứng nhận VNU-EPT và Chứng chỉ VSTEP quốc gia (Vietnamese Standardized Test of English Proficiency): Xét miễn môn Anh Văn 1,2,3,4 cho SV khoá 2020 về trước hoặc SV từ khoá 2021 về sau (trong thời hạn không quá 01 năm).
Thông tin CCNN sẽ được gửi đến cơ quan tổ chức thi để thẩm tra, mọi gian lận sẽ bị xử lý kỷ luật (buộc tạm dừng học, buộc thôi học). Ngoài ra còn phải chịu hình thức kỷ luật từ đơn vị cấp chứng chỉ.
Sinh viên vui lòng xem Quy chế học vụ đào tạo tại hcmut.edu.vn >> Đào tạo >> Quy chế - quy định >> Quy định về học vụ và đào tạo bậc đại học – Phiên bản hợp nhất/ Phụ lục 7. Quy định về chuẩn ngoại ngữ dành cho chương trình giảng dạy bằng tiếng Việt/ 1. Chuẩn ngoại ngữ từng năm; 2. Chuẩn ngoại ngữ tốt nghiệp; 3. Quy đổi các bằng cấp & CCNN.
 3. Thời gian nộp: 

Chuẩn ngoại ngữ từng năm: SV phải đăng ký thông tin nộp CCNN/ Xét miễn theo Lịch đăng ký môn học mỗi học kỳ tại tại trang web hcmut.edu.vn >> Đào tạo >> Lịch học vụ. 
Đăng ký LVTN/KLTN: SV phải đăng ký thông tin nộp CCNN theo Lịch đăng ký môn học mỗi học kỳ tại tại trang web hcmut.edu.vn >> Đào tạo >> Lịch học vụ. Tại thời điểm xét LVTN/KLTN, chấp nhận CCNN mà SV đã đăng ký (chưa thẩm tra). PĐT sẽ thẩm tra và hậu kiểm, nếu SV đăng ký không đúng thì LVTN/KLTN sẽ bị hủy và SV sẽ bị xử lý kỷ luật. Xem thời hạn đăng ký LVTN/KLTN tại Lịch đăng ký môn học.
Xét tốt nghiệp: SV đăng ký nộp CCNN và sau khi CCNN được thẩm tra hợp lệ thì SV đăng ký xét tốt nghiệp bổ sung tại trang web Mybk.hcmut.edu.vn >> Hỗ trợ trực tuyến (Bksi) >> Tốt nghiệp. SV nên nộp CCNN trước hạn chót đăng ký và nộp hồ sơ tốt nghiệp khoảng 2 tuần. Xem thời hạn đăng ký tốt nghiệp tại thông tin tốt nghiệp trang web (hcmut.edu.vn) >> Đào tạo >> Lịch học vụ >> Lịch tốt nghiệp.
 4. Riêng Bằng Tú tài Pháp, TCF và DEFL: 

    Do trường Đại học Sư phạm Tp.HCM giới hạn về thời gian nhận thẩm tra các văn bằng tiếng Pháp nên Nhà trường chỉ tiến hành thẩm tra chứng chỉ tiếng Pháp cuối mỗi tháng.

    Nên SV phải Đăng ký nộp Chứng chỉ ngoại ngữ  ngay khi có  chứng chỉ (văn bằng tiếng Pháp) để Nhà trường thẩm tra kịp thời.

 II. Kiểm tra trình độ Tiếng Anh định kỳ:

 Đối với Khóa 2020 trở về trước: Kết quả thi kiểm tra trình độ tiếng Anh dùng xét đạt chuẩn ngoại ngữ từng năm học, không dùng để xét miễn / miễn điểm / xét lớp các môn anh văn.

Kỳ kiểm tra Anh văn định kỳ HK221 đã dùng để xét chuẩn Anh văn từng năm, Phòng Đào tạo sẽ không tổ chức kiểm tra anh văn định kỳ theo qui chế. SV có thể đăng ký học các môn Anh văn hoặc nộp CCNN để xét miễn các môn AV và để đạt chuẩn ngoại ngữ từng năm.
III. Kiểm tra trình độ tiếng Anh đầu vào: (áp dụng cho SV từ khóa 2021 trở về sau)

Sau khi nhập học, Nhà trường tổ chức một kỳ kiểm tra trình độ tiếng Anh đầu vào theo định dạng Toeic dành cho các sinh viên chính quy vừa trúng tuyển. Kết quả kiểm tra sẽ được dùng để xét miễn một lần duy nhất các học phần tiếng Anh tương ứng. Các học phần không được miễn, sinh viên phải đăng ký học (Anh văn 1,2,3,4). Sinh viên vừa trúng tuyển, trong thời hạn không quá 01 năm (SV khóa 2021, khóa 2022 hạn cuối nộp CCNN để đăng ký xét miễn và phải hoàn tất thanh toán lệ phí xét miễn đến hết ngày 30/09/2023), có thể dùng chứng chỉ Ngoại ngữ quốc tế còn thời hạn phù hợp để được xét miễn các học phần tiếng Anh (theo quy định Điều 3. Quy đổi các bằng cấp và chứng chỉ ngoại ngữ) và đồng thời có thể được xét đạt chuẩn ngoại ngữ tốt nghiệp (theo quy định Điều 2. Chuẩn ngoại ngữ tốt nghiệp)
Sinh viên vui lòng xem Quy chế học vụ đào tạo tại hcmut.edu.vn >> Đào tạo >> Quy chế - quy định >> Quy định về học vụ và đào tạo bậc đại học – Phiên bản hợp nhất/ Phụ lục 7. Quy định về chuẩn ngoại ngữ dành cho chương trình giảng dạy bằng tiếng Việt/1. Chuẩn ngoại ngữ từng năm; 2. Chuẩn ngoại ngữ tốt nghiệp; 3. Quy đổi các bằng cấp & CCNN
 IV. Các câu hỏi khác: 

1. Nếu em nộp chứng chỉ toeic 2 kĩ năng nghe và đọc sau ngày 29/8 vậy thì anh văn em được tính là đạt, vậy thì em có được tính 8 chỉ anh văn đó vào số tín chỉ tích lũy không ạ?

Từ HK 221, Các chứng chỉ tiếng Anh quốc tế được quy đổi tương đương: Đạt, Các môn được xét miễn được ghi điểm vào mục điểm chuyển/bảo lưu trên bảng điểm, SV sẽ nhận điểm miễn các học phần gốc, tính tích lũy tín chỉ, không tính vào điểm trung bình tích lũy.
2. Môn anh văn theo nhu cầu (Anh văn 1A, 2A, 3A, 4A) đăng ký và cách tính điểm như thế nào?

Thông tin chi tiết về các lớp Anh văn theo yêu cầu, SV vui lòng tham khảo tại link sau  http://www.bkenglish.edu.vn.
Đăng ký tại: hcmut.edu.vn>> chọn  Đăng ký môn học >> chọn Đăng ký bổ sung các lớp Anh văn theo yêu cầu khai giảng ngày …
Xem chi tiết các đợt đăng ký môn học Anh văn theo nhu cầu tại trang web hcmut.edu.vn >> Đào tạo >> Lịch học vụ.
Môn Anh văn theo nhu cầu sẽ tính ĐẠT các môn anh văn tương ứng (Anh văn 1, 2, 3, 4), tính tích lũy tín chỉ, không tính vào điểm trung bình tích lũy.
SV học ĐẠT môn Anh văn theo nhu cầu sẽ tính ĐẠT các môn anh văn tương ứng (Anh văn 1, 2, 3, 4), sau đó sẽ tính vào số tích lũy tín chỉ chung
Môn Anh văn theo nhu cầu số tín chỉ là 0 nên không tính số tín chỉ học kỳ và không tính vào điểm trung bình học kỳ. Tuy nhiên sẽ được đặc cách tính vào tổng số tín chỉ đăng ký của học kỳ khi xét Số tín chỉ đăng ký tối thiểu trong một học kỳ khi Xử lý học vụ
Học phí các lớp Anh văn theo nhu cầu tính theo học phí dự thính: Về thông tin học phí bạn vui lòng xem chi tiết tại trang web trang hcmut.edu.vn >> Đào tạo >>học phí >> Mức thu học phí các bậc đào tạo năm 2022-2023.
3. Sinh viên không đăng ký môn học được vì báo thiếu chuẩn anh văn hàng năm (CCAS_0, CCAS_1, CCAS_2, CCAS_3)?

Sinh viên xem chi tiết tại: Bảng giải thích ký hiệu các chuẩn.
Sinh viên vui lòng xem Quy chế học vụ đào tạo tại hcmut.edu.vn >> Đào tạo >> Quy chế - quy định >> Quy định về học vụ và đào tạo bậc đại học – Phiên bản hợp nhất/ Phụ lục 7. Quy định về chuẩn ngoại ngữ dành cho chương trình giảng dạy bằng tiếng Việt/1. Chuẩn ngoại ngữ từng năm.
4. Sinh viên không đăng ký môn học được vì báo thiếu chuẩn sinh viên hàng năm SV_N2, SV_N3, SV_N4?

Sinh viên xem chi tiết tại: Bảng giải thích ký hiệu các chuẩn.
Điều kiện để đạt chuẩn sinh viên các năm tại Điều 9- XẾP TRÌNH ĐỘ NĂM HỌC CỦA SINH VIÊN, Quyết định ban hành Quy định về học vụ và đào tạo bậc đại học (số 2933 ngày 10/9/21). Bao gồm phải đạt số tín chỉ tích lũy theo quy định + đạt chuẩn ngoại ngữ theo quy định, ngoài ra để có thể xếp trình độ từ năm thứ ba SV phải hoàn thành chương trình Giáo dục Quốc phòng – An ninh và Giáo dục thể chất.
5. SV làm thế nào để đạt chuẩn ngoại ngữ từng năm học?

+ Học đạt các môn anh văn (1, 2, 3, 4), Ngoài ra trong các học kỳ vừa qua, Nhà trường tổ chức các lớp Anh văn học theo nhu cầu để hỗ trợ SV trong việc hoàn tất các học phần Anh văn.

+ Đăng ký nộp CCNN quốc tế và đăng ký miễn điểm anh văn theo quy định.

+ Đối với SV từ khóa 2020 trở về trước: Kỳ kiểm tra Anh văn định kỳ HK221 đã dùng để xét chuẩn Anh văn từng năm, Phòng Đào tạo sẽ không tổ chức kiểm tra anh văn định kỳ theo qui chế. SV có thể đăng ký học các môn Anh văn hoặc nộp CCNN để xét miễn các môn AV và để đạt chuẩn ngoại ngữ từng năm.

+ Đối với SV từ khóa 2021 trở về sau: Sau khi nhập học, Nhà trường tổ chức một kỳ kiểm tra trình độ tiếng Anh đầu vào theo định dạng Toeic dành cho các sinh viên chính quy vừa trúng tuyển. Kết quả kiểm tra sẽ được dùng để xét miễn một lần duy nhất các học phần tiếng Anh tương ứng.

6. SV làm thế nào để đạt cá môn anh văn (1, 2, 3, 4)?

+ Đăng ký học các môn anh văn (1, 2, 3, 4) theo chương trình đào tạo.

+ Đăng ký học các lớp Anh văn học theo nhu cầu (Anh văn 1A, 2A, 3A, 4A). Anh văn theo yêu cầu 1A, 2A, 3A, 4A sẽ tính ĐẠT các môn anh văn tương ứng, tính tích luỹ tín chỉ, không tính vào điểm trung bình tích lũy

+ Đăng ký nộp CCNN quốc tế và xét miễn các môn anh văn theo đúng quy định.

7. Chuẩn tốt nghiệp:

Sinh viên vui lòng xem Quy chế học vụ đào tạo tại hcmut.edu.vn >> Đào tạo >> Quy chế - quy định >> Quy định về học vụ và đào tạo bậc đại học – Phiên bản hợp nhất/ Phụ lục 7. Quy định về chuẩn ngoại ngữ dành cho chương trình giảng dạy bằng tiếng Việt/ 2. Chuẩn ngoại ngữ tốt nghiệp.

2 kỹ năng Nói – Viết: Tạm thời cho phép sinh viên dùng kết quả các ký kiểm tra kỹ năng Nói – Viết do Trung tâm Ngoại ngữ Trường Đại học Bách Khoa tổ chức để xét tốt nghiệp. Yêu cầu mức tối thiểu là mức “Đạt”, tương đương mức điểm 200, riêng chương trình tài năng & chương trình Kỹ sư Việt-Pháp là mức “Đạt” tương đương mức điểm 245.

8. Bảng quy đổi điểm chứng chỉ VSTEP, VNU-EPT với các môn Anh văn:

 Lưu ý: Chỉ xét miễn các môn Anh văn 1, 2, 3, 4 cho SV khóa 2020 về trước & SV từ khóa 2021 về sau (áp dụng cho năm học đầu tiên). Không dùng để xét chuẩn tốt nghiệp. Theo thông báo "CÁC THAY ĐỔI CHÍNH VỀ HỌC VỤ TỪ HK222"

 

Chứng chỉ VSTEP
4.0 Anh văn 1(Đạt)
4.5 Anh văn 1(Đạt) Anh văn 2(Đạt)
5.0 Anh văn 1(Đạt) Anh văn 2(Đạt) Anh văn 3(Đạt)
5.5 Anh văn 1(Đạt) Anh văn 2(Đạt)  Anh văn 3(Đạt) Anh văn 4(Đạt)


Chứng chỉ VNU-  EPT

200 Anh văn Cơ bản(Đạt)
218 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt)
234 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt)
250 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt) Anh văn 3(Đạt)
260 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt)  Anh văn 3(Đạt) Anh văn 4(Đạt)
270 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt)  Anh văn 3(Đạt) Anh văn 4(Đạt)
280 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt)  Anh văn 3(Đạt) Anh văn 4(Đạt)
290 Anh văn Cơ bản(Đạt) Anh văn 1(Đạt) Anh văn 2(Đạt)  Anh văn 3(Đạt) Anh văn 4(Đạt)

 
9: Chứng chỉ TCF: 

BẢNG QUY ĐỔI TƯƠNG ĐƯƠNG: xét chuẩn ngoại ngữ tốt nghiệp

 

 KNLNNVN

 Tiếng Pháp

 Bậc 3 (CEFR B1) DELF B1 TCF B1

 Bậc 4 (CEFR B2) DELF B2TCF B2

 

Bảng quy đổi văn bằng DELF, chứng chỉ TCF với các môn Pháp văn:

A1 100-199 Pháp văn 1(Đạt)
A2 200-299 Pháp văn 1(Đạt) Pháp văn 2(Đạt)
B1 300-399 Pháp văn 1(Đạt) Pháp văn 1(Đạt) Pháp văn 2(Đạt) Pháp văn 3(Đạt) Pháp văn 4(Đạt) Pháp văn 5(Đạt) Pháp văn 6(Đạt) Pháp văn 7*(Đạt)

*Pháp văn 7: áp dụng cho sinh viên Khóa 2018 về trước."""

# Tạo một dictionary chứa văn bản và đặt nó vào một cặp key-value
data = {"text": text}

# Chuyển đổi dữ liệu thành định dạng JSON
json_data = json.dumps(data, ensure_ascii=False)

# In ra kết quả JSON
print(json_data)
