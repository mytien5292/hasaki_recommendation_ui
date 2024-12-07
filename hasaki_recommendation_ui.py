import numpy as np
import pandas as pd
import streamlit as st
import json
import time

DEFAULT_IMAGE = "https://media.hcdn.vn/catalog/product/k/e/kem-chong-nang-skin1004-cho-da-nhay-cam-spf-50-50ml_img_800x800_eb97c5_fit_center.jpg"
DEFAULT_PRODUCT_LINK = "https://hasaki.vn/san-pham/kem-chong-nang-skin1004-chiet-xuat-rau-ma-spf50-pa-50ml-86167.html"

# ======= Load data part =======
@st.cache_data
def load_data_recommendation():
    data = pd.read_csv('data/all_user_recommendations.csv')
    return data

@st.cache_data
def load_data_products():
    data = pd.read_csv('data/san_pham_processed.csv')
    return data

@st.cache_data
def load_popular_products():
    data = pd.read_csv('data/most_reviewed_products.csv')
    return data

@st.cache_data
def load_similar_products():
    data = pd.read_csv('data/all_similarity_products.csv')
    data["ma_san_pham"] = data["ma_san_pham"].astype(str)
    return data

# ======= Recommendation part =======
def get_user_recommendations(user_id):
    if "data_recommendation" not in st.session_state:
        st.session_state.data_recommendation = load_data_recommendation()

    data_recommendation = st.session_state.data_recommendation

    user_data = data_recommendation[data_recommendation['user_id'] == user_id]
    history_products = user_data['history'].values
    recommendation_products = user_data['recommendations'].values

    return history_products, recommendation_products

def get_similar_products(product_id):
    if "data_similar_products" not in st.session_state:
        st.session_state.data_similar_products = load_similar_products()
    
    data_similar_products = st.session_state.data_similar_products
    product_ids = data_similar_products[data_similar_products['ma_san_pham'] == str(product_id)]['similarity_products'].values

    return product_ids

def get_product_info(product_ids):
    if "data_products" not in st.session_state:
        st.session_state.data_products = load_data_products()
    
    data_products = st.session_state.data_products
    data_products["hinh_san_pham"] = DEFAULT_IMAGE
    data_products["link_san_pham"] = DEFAULT_PRODUCT_LINK

    product_info = data_products[data_products['ma_san_pham'].isin(product_ids)]

    return product_info

# ======= UI part =======
def show_list_products_info(product_ids):
    product_infos = get_product_info(product_ids)
    index_counter = 0
    col1, col2 = st.columns(2)
    for product_row in product_infos.itertuples():
        similar_products_ids = get_similar_products(product_row.ma_san_pham)
        similar_products_ids = json.loads(similar_products_ids[0])
        similar_products_ids = similar_products_ids[1:]
        similar_products_infos = get_product_info(similar_products_ids)

        if index_counter % 2 == 0:
            with col1:
                show_product_info(product_row, similar_products_infos)
        else:
            with col2:
                show_product_info(product_row, similar_products_infos)
        
        index_counter += 1

def show_product_info(product_info, similar_products_infos):
    #st.write(f"""##### {product_info.ten_san_pham}\n""")
    st.markdown(
    f"""
    <h5 style='color: green;'>{product_info.ten_san_pham}</h5>
    """,
    unsafe_allow_html=True,
)
    st.image(product_info.hinh_san_pham, width=200)
    st.write(f"""[Xem chi tiết sản phẩm]({product_info.link_san_pham})""")
    
    formatted_price = f"{product_info.gia_ban:,}đ"
    st.markdown(
        f"""
        **Mã sản phẩm**: {product_info.ma_san_pham}  
        **Giá bán**: <span style='color: red;'>{formatted_price}</span>  
        
        **Điểm trung bình**: {product_info.diem_trung_binh} ⭐
        """,
        unsafe_allow_html=True,
    )

    show_similar_products(similar_products_infos)

    st.write("---")

def show_similar_products(similar_products_infos):
    similar_items = st.expander("Sản phẩm tương tự")

    for product_info in similar_products_infos.itertuples():
        # Toàn bộ thông tin sản phẩm trong khung với nền xanh lục nhạt
        similar_items.markdown(
            f"""
            <div style='background-color: #e6ffe6; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                <h5 style='color: green;'>{product_info.ten_san_pham}</h5>
                <img src="{product_info.hinh_san_pham}" width="100">
                <p><a href="{product_info.link_san_pham}" target="_blank">Xem chi tiết sản phẩm</a></p>
                <p><b>Mã sản phẩm</b>: {product_info.ma_san_pham}</p>
                <p><b>Giá</b>: <span style='color: red;'>{product_info.gia_ban:,}đ</span></p>
                <p><b>Điểm trung bình</b>: {product_info.diem_trung_binh} ⭐</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Ngăn cách giữa các sản phẩm
        similar_items.write("---")

def business_objective_content():
    st.image("media/hasaki_banner.jpg", width=800)
    #st.subheader("Đặt vấn đề")
    # Tiêu đề chính và các tiêu đề phụ với màu xanh lục
    st.markdown(
        """
        <h3 style='color: green;'>1. Giới thiệu bài toán Recommendation sản phẩm mỹ phẩm cho Hasaki</h3>
        """,
        unsafe_allow_html=True,
    )

    # Nội dung dưới tiêu đề chính
    st.write("""
    Trong lĩnh vực thương mại điện tử mỹ phẩm, việc cá nhân hóa trải nghiệm mua sắm là chìa khóa giúp nâng cao sự hài lòng của khách hàng và tối ưu doanh thu. Với danh mục sản phẩm đa dạng từ chăm sóc da, trang điểm đến dưỡng tóc, **Hasaki.vn** cần một hệ thống gợi ý sản phẩm thông minh để hỗ trợ khách hàng tìm kiếm và lựa chọn sản phẩm phù hợp.
    """)

    # Tiêu đề "2. Mục tiêu của hệ thống Recommendation:" với màu xanh lục
    st.markdown(
        """
        <h3 style='color: green;'>2. Mục tiêu của hệ thống Recommendation</h3>
        """,
        unsafe_allow_html=True,
    )

    # Nội dung dưới tiêu đề phụ
    st.write("""
    - **Cá nhân hóa**: Đề xuất sản phẩm dựa trên sở thích và hành vi của khách hàng.
    - **Tăng tỷ lệ chuyển đổi**: Gợi ý sản phẩm liên quan và thúc đẩy bán chéo.
    - **Độ chính xác cao**: Ứng dụng các phương pháp như Collaborative Filtering, Content-Based Filtering, và Hybrid.
    """)

    # Tiêu đề "3. Lợi ích cho Hasaki:" với màu xanh lục
    st.markdown(
        """
        <h3 style='color: green;'>3. Lợi ích cho Hasaki</h3>
        """,
        unsafe_allow_html=True,
    )

    # Nội dung dưới tiêu đề phụ
    st.write("""
    - Cải thiện trải nghiệm khách hàng.
    - Tối ưu hóa chiến lược kinh doanh.
    - Khẳng định vị thế dẫn đầu trong ngành mỹ phẩm tại Việt Nam.
    """)

def build_project_content():
   # st.subheader("Thực hiện dự án")
   # 1. cào dữ liệu
    st.markdown(
    """
    <h3 style='color: green;'>1. Crawl thêm dữ liệu</h3>
    """,
    unsafe_allow_html=True,
)
    st.image("media/crawl_them_du_lieu.jpg", width=600)
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 2. Tiền xử lý dữ liệu
    st.markdown(
    """
    <h3 style='color: green;'>2. Tiền xử lý dữ liệu</h3>
    """,
    unsafe_allow_html=True,
)
    st.write("""
            - Bỏ các bình luận bị duplicate hoặc nan
            - Bỏ các dấu space, khoảng trắng dư thừa
            - Thay thế kí tự emoji
            - Thay thế các từ tiếng Anh thành tiếng Việt
            - Thay thế các từ teencode thành từ đọc được
            - Bỏ các stopword
""")
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 3.phân tích dữ liệu
    st.markdown(
    """
    <h3 style='color: green;'>3. Phân tích dữ liệu</h3>
    """,
    unsafe_allow_html=True,
)
    st.write("#### Số lượng review của từng users") 
    st.image("media/so_luong_review_tren_tung_user.jpg", width=600)

    st.write("#### Các sản phẩm thường được mua chung") 
    st.image("media/cac_san_pham_thuong_duoc_mua_chung.jpg", width=600)

    st.write("#### Sản phẩm phổ biến nhất ở mỗi tháng") 
    st.image("media/san_pham_pho_bien_nhat_moi_thang.jpg", width=600)

    st.write("#### Số tháng liên tiếp sản phẩm đạt 'Sản phẩm phổ biến nhất ở mỗi tháng - 'Streak'") 
    st.image("media/top_5_san_pham_co_treak_cao_nhat.jpg", width=600)
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 4.Gensim và Cosine
    st.markdown(
    """
    <h3 style='color: green;'>4. Xây dựng model bằng Content Base: Gensim và Cosine Similarity</h3>
    """,
    unsafe_allow_html=True,
)

    st.markdown(
    """
    <ul style='margin-left: 20px;'>
        <li>Input: Sản phẩm: 422210557 - Combo 2 Nước Dưỡng Tóc Cocoon Tinh Dầu Bưởi Phiên Bản Mới 140ml.  </li>
        <li>Output: Xuất ra các sản phẩm có nội dung tương tự, có số sao từ 4.0 trở lên.</li>
    </ul>
    """,
    unsafe_allow_html=True,
)
    st.image("media/gensim_cosine_ket_qua.jpg", width=600)

    st.markdown(
        """
        <span style='font-size: 20px; color: black;'>Kết luận:</span>
        <ul style='margin-left: 20px;'>
            <li>Cả Gensim và Cosine Similarity đều cho ra kết quả gợi ý cho mã sản phẩm 422210557 giống nhau.</li>
            <li>Lựa chọn thuật toán Cosine Similarity cho bài toán gợi ý người dùng vì quy mô dữ liệu nhỏ, chỉ tính toán đơn giản về độ tương đồng của 2 vector, thời gian thực hiện nhanh.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 5. Surprise, LightFM và ALS
    st.markdown(
    """
    <h3 style='color: green;'>5. Xây dựng model bằng Collaborative Filtering: Surprise và ALS-PySpark</h3>
    """,
    unsafe_allow_html=True,
)
    st.markdown(
    """
    <ul style='margin-left: 20px;'>
        <li> Input: chọn 1 mã khách hàng nhập vào.  </li>
        <li>Output: Xuất ra các sản phẩm mà khách hàng đã đánh giá và các sản phẩm gợi ý cho khách hàng đó, có số sao từ 4.0 trở lên.</li>
    </ul>
    """,
    unsafe_allow_html=True,
)
    st.write("#### Kết quả gợi ý sản phẩm của phương pháp Surprise:") 
    st.image("media/kq_surprise.jpg", width=600)

    st.write("#### Kết quả gợi ý sản phẩm của phương pháp LightFM:")
    st.image("media/kq_LightFM.jpg", width=600)

    st.write("#### Kết quả gợi ý sản phẩm của phương pháp ALS:")
    st.image("media/kq_ALS.jpg", width=600)

    st.markdown(
        """
        <span style='font-size: 20px; color: black;'>Kết luận:</span>
        <ul style='margin-left: 20px;'>
            <li>Phương pháp Surprise và ALS đều cho kết qủa khá tốt, nhưng sẽ chọn phương pháp ALS vì có hiệu suất cao nhất. </li>
            <li>Phương pháp LightFM có kết quả tệ nhất, cần được cải tiến nhiều hơn nếu muốn sử dụng phương pháp này.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 6. Kết luận chung
    st.markdown(
    """
    <h3 style='color: green;'>6. Kết luận chung</h3>
    """,
    unsafe_allow_html=True,
)
    st.markdown(
    """
    <ul style='margin-left: 20px;'>
        <li> Chọn phương pháp Cosine Similarity nếu muốn dùng Content_based filtering.</li>
        <li> Chọn phương pháp ALS nếu muốn dùng Collaborative filtering. </li>
    </ul>
    """,
    unsafe_allow_html=True,
)
    st.markdown(
    """
    <hr style="border: none; height: 2px; background-color: red;">
    """,
    unsafe_allow_html=True
)
    # 7. Phân công công việc
    st.markdown(
    """
    <h3 style='color: green;'>7. Phân công công việc</h3>
    """,
    unsafe_allow_html=True,
)
    st.image("media/phan_cong_cong_viec.jpg", width=600)
    
#def new_prediction():
    #st.subheader("Thực hiện dự án")
###

def get_popular_products():
    if "popular_products" not in st.session_state:
        st.session_state.popular_products = load_popular_products()
    
    data_products = st.session_state.popular_products
    popular_products = data_products.sort_values(by='month_year', ascending=False).head(10)
    return popular_products['ma_san_pham'].tolist()

def new_prediction_content():
    user_name = st.session_state["username"]
    user_id = int(user_name.split("_")[-1])

    history_products, recommendation_products = get_user_recommendations(user_id)

    if len(history_products) == 0:
        st.write("## Đây là các sản phẩm phổ biến trong thời gian qua mà bạn có thể quan tâm:")
        popular_products = get_popular_products()

        show_list_products_info(popular_products)
    else:
        # Tiêu đề với thẻ h3
        st.markdown(
            """
            <div style="
                background-color: green; 
                color: white; 
                padding: 10px; 
                border-radius: 5px; 
                text-align: center;
            ">
                <h3>Những sản phẩm của Hasaki mà bạn đã tin dùng!</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # historical data
        history_products = json.loads(history_products[0])
        show_list_products_info(history_products)

        #st.write("## Tôi nghĩ bạn cũng sẽ thích những sản phẩm này:")
        st.markdown(
            """
            <div style="
                background-color: green; 
                color: white; 
                padding: 10px; 
                border-radius: 5px; 
                text-align: center;
            ">
                <h3>Gợi ý của Hasaki dành cho bạn!</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # recommendation
        recommendation_products = json.loads(recommendation_products[0])
        show_list_products_info(recommendation_products)

        

# ======= Main content =======
def main_content():
    # Tiêu đề với màu xanh lục
    st.markdown(
        """
        <h1 style='color: green;'>Gợi ý sản phẩm cho Hasaki</h1>
        """,
        unsafe_allow_html=True,
    )
    #st.subheader("Thực hiện dự án")
###

 ###
       # Tiêu đề Menu
    st.sidebar.markdown(
        """
        <div style='color: green; font-size: 18px; font-weight: bold; margin-bottom: -20px;'>
            Menu
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Menu chính
    menu = ["Đặt vấn đề", "Thực hiện dự án", "Dự đoán mới"]
    choice = st.sidebar.selectbox("", menu)

    # Tiêu đề Thành viên thực hiện
    st.sidebar.markdown("""
    <div style="color: green; font-size: 16px; font-weight: bold; margin-top: 20px;">
        Thành viên thực hiện:
    </div>
    """, unsafe_allow_html=True)

    # Hiển thị ảnh Nguyễn Thị Mỷ Tiên
    st.sidebar.image("media/tien.jpg", width=150, caption="Nguyễn Thị Mỷ Tiên", use_container_width=False)

    # Hiển thị ảnh Đặng Thị Thảo
    st.sidebar.image("media/thao.jpg", width=150, caption="Đặng Thị Thảo", use_container_width=False)
    
    # Giảng viên hướng dẫn
    st.sidebar.markdown("""
    <div style="color: green; font-size: 16px; font-weight: bold; margin-top: 20px;">
        Giảng viên hướng dẫn:
    </div>
    """, unsafe_allow_html=True)
    # Hiển thị ảnh giảng viên
    st.sidebar.image("media/co_phuong.jpg", width=150, caption="Cô Khuất Thuỳ Phương", use_container_width=False)
    
    # Thời gian thực hiện
    st.sidebar.markdown("""
    <div style="color: green; font-size: 16px; font-weight: bold; margin-top: 20px;">
        Thời gian thực hiện:
    </div>
    <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9; margin-top: 5px;">
        16/12/2024
    </div>
    """, unsafe_allow_html=True) 

    if choice == 'Đặt vấn đề':
        business_objective_content()
    elif choice == 'Thực hiện dự án':
        build_project_content()
    elif choice == 'Dự đoán mới':
        new_prediction_content()