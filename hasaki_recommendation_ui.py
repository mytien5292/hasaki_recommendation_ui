import numpy as np
import pandas as pd
import streamlit as st
import json

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
    st.write(f"""##### {product_info.ten_san_pham}\n""")
    st.image(product_info.hinh_san_pham, width=200)
    st.write(f"""[Xem chi tiết sản phẩm]({product_info.link_san_pham})""")
    
    formatted_price = f"{product_info.gia_ban:,}đ"
    st.write(f"""
        **Mã sản phẩm**: {product_info.ma_san_pham}\n
        **Giá**: {formatted_price}\n
        **Điểm trung bình**: {product_info.diem_trung_binh} ⭐\n
    """)

    show_similar_products(similar_products_infos)

    st.write("---")

def show_similar_products(similar_products_infos):
    similar_items = st.expander("Sản phẩm tương tự")

    for product_info in similar_products_infos.itertuples():
        similar_items.write(f"""##### {product_info.ten_san_pham}\n""")
        similar_items.image(product_info.hinh_san_pham, width=100)
        similar_items.write(f"""[Xem chi tiết sản phẩm]({product_info.link_san_pham})""")
    
        formatted_price = f"{product_info.gia_ban:,}đ"
        similar_items.write(f"""
            **Mã sản phẩm**: {product_info.ma_san_pham}\n
            **Giá**: {formatted_price}\n
            **Điểm trung bình**: {product_info.diem_trung_binh} ⭐\n
        """)

        similar_items.write("---")

def business_objective_content():
    st.subheader("Business Objective")
    st.write("""
        ## Giới thiệu bài toán Recommendation sản phẩm mỹ phẩm cho Hasaki

        Trong lĩnh vực thương mại điện tử mỹ phẩm, việc cá nhân hóa trải nghiệm mua sắm là chìa khóa giúp nâng cao sự hài lòng của khách hàng và tối ưu doanh thu. Với danh mục sản phẩm đa dạng từ chăm sóc da, trang điểm đến dưỡng tóc, **Hasaki** cần một hệ thống gợi ý sản phẩm thông minh để hỗ trợ khách hàng tìm kiếm và lựa chọn sản phẩm phù hợp.

        ### Mục tiêu của hệ thống Recommendation:
        - **Cá nhân hóa**: Đề xuất sản phẩm dựa trên sở thích và hành vi của khách hàng.
        - **Tăng tỷ lệ chuyển đổi**: Gợi ý sản phẩm liên quan và thúc đẩy bán chéo.
        - **Độ chính xác cao**: Ứng dụng các phương pháp như Collaborative Filtering, Content-Based Filtering, và Hybrid.

        ### Lợi ích cho Hasaki:
        - Cải thiện trải nghiệm khách hàng.
        - Tối ưu hóa chiến lược kinh doanh.
        - Khẳng định vị thế dẫn đầu trong ngành mỹ phẩm tại Việt Nam.
    """) 

def build_project_content():
    st.subheader("Build Project")
    st.write("##### 1. Some data")
    st.write("##### 2. Visualize Ham and Spam")
    st.write("##### 3. Build model...")
    st.write("##### 4. Evaluation")
    st.write("##### 5. Summary: This model is good enough for Ham vs Spam classification.")

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
        st.write("## Vì bạn đã đánh giá các sản phẩm sau:")
        # historical data
        history_products = json.loads(history_products[0])
        show_list_products_info(history_products)

        st.write("## Tôi nghĩ bạn cũng sẽ thích những sản phẩm này:")
        # recommendation
        recommendation_products = json.loads(recommendation_products[0])
        show_list_products_info(recommendation_products)

# ======= Main content =======
def main_content():
    st.title("Gợi ý sản phẩm cho Hasaki")

    menu = ["Business Objective", "Build Project", "New Prediction"]
    choice = st.sidebar.selectbox('Menu', menu)
    st.sidebar.write("""#### Thành viên thực hiện:
                    Tiên và Thảo""")
    st.sidebar.write("""#### Giảng viên hướng dẫn: Cô Khuất Thuỳ Phương""")
    st.sidebar.write("""#### Thời gian thực hiện: 12/2024""")

    if choice == 'Business Objective':
        business_objective_content()
    elif choice == 'Build Project':
        build_project_content()
    elif choice == 'New Prediction':
        new_prediction_content()