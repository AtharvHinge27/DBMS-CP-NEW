-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 08_sample_seed_data.sql
-- Description: Comprehensive, realistic seed data across all modules
-- ============================================================================

USE innosphere_db;

-- ----------------------------------------------------------------------------
-- 1. Seed Colleges
-- ----------------------------------------------------------------------------
INSERT INTO colleges (college_id, college_code, college_name, city, state, website) VALUES
(1, 'PICT-PUN', 'Pune Institute of Computer Technology', 'Pune', 'Maharashtra', 'https://pict.edu'),
(2, 'COEP-PUN', 'COEP Technological University', 'Pune', 'Maharashtra', 'https://coep.org.in'),
(3, 'VJTI-MUM', 'Veermata Jijabai Technological Institute', 'Mumbai', 'Maharashtra', 'https://vjti.ac.in');

-- ----------------------------------------------------------------------------
-- 2. Seed Departments
-- ----------------------------------------------------------------------------
INSERT INTO departments (department_id, college_id, department_code, department_name) VALUES
(1, 1, 'COMP', 'Computer Engineering'),
(2, 1, 'IT', 'Information Technology'),
(3, 1, 'AIDS', 'Artificial Intelligence & Data Science'),
(4, 1, 'ENTC', 'Electronics & Telecommunication'),
(5, 2, 'CSE', 'Computer Science & Engineering'),
(6, 2, 'IT', 'Information Technology'),
(7, 3, 'COMP', 'Computer Engineering'),
(8, 3, 'IT', 'Information Technology');

-- ----------------------------------------------------------------------------
-- 3. Seed Users
-- Passwords:
-- admin@innosphere.edu -> admin123
-- coord@pict.edu -> coord123
-- mentor@innosphere.edu -> mentor123
-- judge.sharma@innosphere.edu -> judge123
-- judge.patil@innosphere.edu -> judge123
-- student users -> student123
-- ----------------------------------------------------------------------------
INSERT INTO users (user_id, college_id, full_name, email, password_hash, role) VALUES
(1, 1, 'System Administrator', 'admin@innosphere.edu', 'scrypt:32768:8:1$WpTHcpUb2IuCa7MU$0c68ac7c268651aff493592be9997550b61a3e9af4f7cb064be3650c737de7315ae38d3932fe57772d0cc594dd7f889c8d3f80a9b3d24039ef25dd3a1e97ae37', 'Admin'),
(2, 1, 'Prof. Rajesh Kulkarni', 'coord@pict.edu', 'scrypt:32768:8:1$z9a4oLAT28ssZIyB$62cf0698f92c882c7730d11efe92a33880c6e102f9382c302b93bf27307b8498a6c6dcce9de7c98ddee3760de4a0bd01637b7755fc86ce0567917f6b69ed7218', 'College Coordinator'),
(3, 1, 'Dr. Sunita Deshmukh', 'mentor@innosphere.edu', 'scrypt:32768:8:1$UOpOvqUkZRBMV2pD$4b69b7a06aa860f45447e6f4f5a6170deb625b573818c9ee60b1ce119b50603ca75c219a5a7fcb4a01936f5984a92bd2d2fa4b2025fb2af18b34151f5739d766', 'Mentor'),
(12, 1, 'Prof. Arvind Sen', 'arvind.sen@pict.edu', 'scrypt:32768:8:1$UOpOvqUkZRBMV2pD$4b69b7a06aa860f45447e6f4f5a6170deb625b573818c9ee60b1ce119b50603ca75c219a5a7fcb4a01936f5984a92bd2d2fa4b2025fb2af18b34151f5739d766', 'Mentor'),
(13, 2, 'Dr. Meera Kulkarni', 'meera.k@coep.ac.in', 'scrypt:32768:8:1$UOpOvqUkZRBMV2pD$4b69b7a06aa860f45447e6f4f5a6170deb625b573818c9ee60b1ce119b50603ca75c219a5a7fcb4a01936f5984a92bd2d2fa4b2025fb2af18b34151f5739d766', 'Mentor'),
(14, 3, 'Er. Shailesh Verma', 'shailesh.v@vjti.ac.in', 'scrypt:32768:8:1$UOpOvqUkZRBMV2pD$4b69b7a06aa860f45447e6f4f5a6170deb625b573818c9ee60b1ce119b50603ca75c219a5a7fcb4a01936f5984a92bd2d2fa4b2025fb2af18b34151f5739d766', 'Mentor'),
(4, 2, 'Dr. Anand Sharma', 'judge.sharma@innosphere.edu', 'scrypt:32768:8:1$TBwyZ8ES8RcQIa2Q$6f68828f73cd984444b99778455f99bb77758425128547c1ac88c9524c1f202c5da3fe5bd669ebc0bce58001ab5b8132c4357814790b9016970b2b586725bca0', 'Judge'),
(5, 1, 'Er. Vikram Patil', 'judge.patil@innosphere.edu', 'scrypt:32768:8:1$TBwyZ8ES8RcQIa2Q$6f68828f73cd984444b99778455f99bb77758425128547c1ac88c9524c1f202c5da3fe5bd669ebc0bce58001ab5b8132c4357814790b9016970b2b586725bca0', 'Judge'),
-- Participants
(6, 1, 'Atharv Hinge', 'atharv@pict.edu', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant'),
(7, 1, 'Priya Nair', 'priya.nair@pict.edu', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant'),
(8, 1, 'Rohan Joshi', 'rohan.joshi@pict.edu', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant'),
(9, 2, 'Sneha Rao', 'sneha.rao@coep.ac.in', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant'),
(10, 2, 'Amitabh Verma', 'amitabh.v@coep.ac.in', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant'),
(11, 3, 'Kavita Iyer', 'kavita.i@vjti.ac.in', 'scrypt:32768:8:1$nGruOETbgklGrxGU$4a6105cbad17746a9572196fe8f0dd25a121ef53cb997d9c5823f4c81f1b972b0a778ba7f76c6105d1742a0a1407576b3c39b92baecb16998d7e373a163e0151', 'Participant');

-- ----------------------------------------------------------------------------
-- 4. Update Participant Profiles with Real Academic Information
-- (Note: Base profile records were created by trigger trg_after_user_insert)
-- ----------------------------------------------------------------------------
UPDATE participant_profiles SET
    roll_number = 'CE-2024-042',
    department_id = 1,
    branch = 'Computer Engineering',
    year_of_study = 2,
    semester = 4,
    phone_number = '+91 9823412345',
    technical_skills = 'Python, Flask, MySQL, JavaScript, React, Docker',
    interests = 'Full Stack Development, Database Optimization, AI Systems',
    github_url = 'https://github.com/AtharvHinge27',
    linkedin_url = 'https://linkedin.com/in/atharv-hinge',
    bio = 'Second-year CS student passionate about building scalable web platforms and database architectures.',
    profile_completion_pct = 95
WHERE user_id = 6;

UPDATE participant_profiles SET
    roll_number = 'IT-2024-019',
    department_id = 2,
    branch = 'Information Technology',
    year_of_study = 2,
    semester = 4,
    phone_number = '+91 9876543210',
    technical_skills = 'Python, Machine Learning, TensorFlow, SQL',
    interests = 'Computer Vision, Data Analytics, Healthcare AI',
    github_url = 'https://github.com/priyanair',
    linkedin_url = 'https://linkedin.com/in/priya-nair',
    bio = 'Data science enthusiast looking to solve urban healthcare problems.',
    profile_completion_pct = 90
WHERE user_id = 7;

UPDATE participant_profiles SET
    roll_number = 'CE-2024-088',
    department_id = 1,
    branch = 'Computer Engineering',
    year_of_study = 2,
    semester = 4,
    phone_number = '+91 9988776655',
    technical_skills = 'JavaScript, Node.js, Express, MongoDB, TailwindCSS',
    interests = 'Web3, Cloud Computing, Backend Microservices',
    github_url = 'https://github.com/rohanjoshi',
    linkedin_url = 'https://linkedin.com/in/rohan-joshi',
    bio = 'Backend engineer focused on real-time systems and API design.',
    profile_completion_pct = 85
WHERE user_id = 8;

UPDATE participant_profiles SET
    roll_number = 'COEP-CS-104',
    department_id = 5,
    branch = 'Computer Science & Engineering',
    year_of_study = 3,
    semester = 6,
    phone_number = '+91 9765432109',
    technical_skills = 'Flutter, Kotlin, Firebase, MySQL, Python',
    interests = 'Mobile Application Development, IoT, Smart Agriculture',
    github_url = 'https://github.com/sneharao',
    linkedin_url = 'https://linkedin.com/in/sneha-rao',
    bio = 'Building mobile solutions that empower farmers and local communities.',
    profile_completion_pct = 90
WHERE user_id = 9;

UPDATE participant_profiles SET
    roll_number = 'COEP-CS-118',
    department_id = 5,
    branch = 'Computer Science & Engineering',
    year_of_study = 3,
    semester = 6,
    phone_number = '+91 9123456780',
    technical_skills = 'C++, Python, Embedded Systems, ROS',
    interests = 'Robotics, Autonomous Navigation, Edge Computing',
    github_url = 'https://github.com/amitabhv',
    linkedin_url = 'https://linkedin.com/in/amitabh-verma',
    bio = 'Robotics engineer specializing in autonomous path planning and sensor fusion.',
    profile_completion_pct = 80
WHERE user_id = 10;

UPDATE participant_profiles SET
    roll_number = 'VJTI-IT-022',
    department_id = 2,
    branch = 'Information Technology',
    year_of_study = 2,
    semester = 3,
    phone_number = '+91 9543216789',
    technical_skills = 'HTML, CSS, Bootstrap, Figma, UI/UX Design',
    interests = 'User Experience Design, Accessible Web Interfaces',
    github_url = 'https://github.com/kavitaiyer',
    linkedin_url = 'https://linkedin.com/in/kavita-iyer',
    bio = 'Passionate about human-centered design and accessible frontend development.',
    profile_completion_pct = 75
WHERE user_id = 11;

-- Seed Profile Details for Mentors
INSERT INTO participant_profiles (user_id, department_id, branch, technical_skills, interests, bio, profile_completion_pct) VALUES
(3, 1, 'Computer Engineering', 'AI/ML, NLP, Deep Learning, Generative AI, PyTorch', 'Artificial Intelligence, Medical Imaging, AI Ethics', 'Professor and Senior Researcher with 15+ years experience guiding national hackathon teams.', 100),
(12, 1, 'Information Technology', 'Cybersecurity, Network Defense, Penetration Testing, Cryptography', 'Zero Trust Architecture, Threat Intelligence, IoT Security', 'Faculty lead for Cyber Security Club, Certified Ethical Hacker (CEH) and industry consultant.', 100),
(13, 5, 'Computer Science & Engineering', 'Cloud Systems, AWS, Kubernetes, Distributed Systems, Microservices', 'Cloud Architecture, Scalable Backends, DevOps', 'Associate Professor specializing in large-scale cloud native systems and database design.', 100),
(14, 8, 'Computer Engineering', 'Full Stack Web, Node.js, Flask, System Architecture, MySQL, React', 'High-Performance APIs, Distributed Databases, Clean Architecture', 'Industry mentor and full-stack software architect helping teams build production-grade MVPs.', 100);


-- ----------------------------------------------------------------------------
-- 5. Seed Hackathons (Internal & External - 26 Realistic Opportunities)
-- ----------------------------------------------------------------------------
INSERT INTO hackathons (
    hackathon_id, college_id, title, theme, description, 
    hackathon_type, mode, venue, organizer_name, eligibility, 
    external_url, registration_deadline, start_date, end_date, 
    min_team_size, max_team_size, prize_pool, status, created_by
) VALUES
(
    1, 1, 
    'InnoHacks 2026 – AI & Web Innovation Sprint', 
    'AI/ML & Web Development', 
    'A 36-hour internal hackathon focused on developing practical, AI-augmented digital solutions for higher education institutions, smart campuses, and student productivity.',
    'Internal', 'Hybrid', 'PICT Innovation Centre & Virtual', 
    'PICT ACM Student Chapter & InnoSphere Council', 
    'Open to all undergraduate students of affiliated colleges. Teams of 2 to 4 members.',
    NULL, '2026-11-20', '2026-11-25', '2026-11-27', 
    2, 4, '₹50,000 + Merit Certificates', 'Open', 2
),
(
    2, 1, 
    'Campus CleanTech & IoT Ideathon 2026', 
    'Sustainability & CleanTech', 
    'Inter-departmental innovation hackathon to build IoT-driven energy monitors, water tracking dashboards, and eco-friendly waste management solutions for college campuses.',
    'Internal', 'Offline', 'Auditorium Hall B, PICT Campus', 
    'Department of Computer Engineering & Green Club', 
    'First, Second, and Third Year engineering students.',
    NULL, '2026-12-01', '2026-12-05', '2026-12-06', 
    2, 4, '₹25,000 + Incubation Support', 'Open', 2
),
(
    3, NULL, 
    'Smart India Hackathon (SIH) 2026 - Software & Hardware Edition', 
    'Smart Cities & Governance', 
    'Nationwide initiative to provide students with a platform to solve some of the pressing problems faced in our day-to-day lives across central ministries, state departments, and industries.',
    'External', 'Hybrid', 'Multiple Nodal Centers across India', 
    'Ministry of Education Innovation Cell & AICTE', 
    'Students pursuing engineering and technological degree programs across India.',
    'https://www.sih.gov.in', '2026-12-15', '2027-01-10', '2027-01-12', 
    4, 6, '₹1,00,000 per problem statement', 'Open', 1
),
(
    4, NULL, 
    'AICTE ATAL National DeepTech Challenge 2026', 
    'Quantum & DeepTech', 
    'Flagship national competition encouraging student researchers to build proof-of-concepts in Quantum Computing, Cyber-Physical Systems, and Next-Gen Semiconductors.',
    'External', 'Online', 'Virtual AICTE ATAL Portal', 
    'AICTE ATAL Academy', 
    'All AICTE approved institution students and faculty research groups.',
    'https://atalacademy.aicte-india.org', '2026-11-30', '2026-12-10', '2026-12-12', 
    1, 4, '₹75,000 + National Recognition', 'Open', 1
),
(
    5, 2, 
    'COEP MindSpark 2026 – National Technical CodeSprint', 
    'Web & App Development', 
    'Annual flagship inter-college hackathon hosted by COEP Technological University challenging participants to build scalable web apps, microservices, and reactive user interfaces.',
    'Internal', 'Hybrid', 'COEP Main Auditorium, Pune', 
    'COEP Technological University Tech Council', 
    'Open to all engineering students across India.',
    NULL, '2026-11-28', '2026-12-02', '2026-12-04', 
    2, 4, '₹40,000 + Tech Trophies', 'Open', 2
),
(
    6, 3, 
    'VJTI Technovanza HackAI 2026', 
    'AI/ML & Generative AI', 
    'High-octane hackathon challenging engineers to deploy real-time computer vision, predictive neural nets, and multimodal assistive devices for urban public infrastructure.',
    'Internal', 'Hybrid', 'VJTI Quadrangle & Virtual Labs, Mumbai', 
    'VJTI Technovanza Technical Board', 
    'Open to university student teams of 2 to 4 members.',
    NULL, '2026-12-05', '2026-12-12', '2026-12-14', 
    2, 4, '₹60,000 + Industry Mentorship', 'Open', 1
),
(
    7, 1, 
    'PICT Credenz 2026 – Generative AI & Autonomous Agent Sprint', 
    'AI/ML & Generative AI', 
    'Build next-gen autonomous LLM agents, retrieval-augmented generation (RAG) pipelines, and localized language models for regional Indian languages.',
    'Internal', 'Online', 'PICT IEEE Virtual Labs', 
    'PICT IEEE Student Branch', 
    'Second, Third, and Final Year CS/IT/AI students.',
    NULL, '2026-12-10', '2026-12-18', '2026-12-20', 
    1, 3, '₹35,000 + Cloud Compute Credits', 'Open', 2
),
(
    8, NULL, 
    'KAVACH 2026 – National Cyber Security Hackathon', 
    'Cybersecurity & Digital Defense', 
    'Nationwide cybersecurity hackathon by Bureau of Police Research and Development (BPR&D) to identify innovative cybersecurity and digital forensics tools for law enforcement.',
    'External', 'Hybrid', 'New Delhi Nodal Center & Online', 
    'BPR&D, Ministry of Home Affairs & AICTE', 
    'Undergraduate and Postgraduate students across Indian technical institutes.',
    'https://kavach.mic.gov.in', '2026-12-20', '2027-01-05', '2027-01-07', 
    3, 6, '₹1,00,000 per Problem Track', 'Open', 1
),
(
    9, NULL, 
    'RBI HarBinger 2026 – Innovation for Transformation (FinTech)', 
    'FinTech & Blockchain', 
    'Global hackathon by Reserve Bank of India on themes of frictionless payments, CBDC (Digital Rupee) interoperability, and AI fraud prevention in financial ecosystems.',
    'External', 'Online', 'RBI Innovation Hub Virtual Portal', 
    'Reserve Bank of India (RBI)', 
    'Students, innovators, and start-up teams worldwide.',
    'https://harbinger.rbi.org.in', '2026-12-22', '2027-01-15', '2027-01-17', 
    2, 5, '₹40,00,000 Total Prize Pool', 'Open', 1
),
(
    10, NULL, 
    'e-Yantra Robotics & Embedded Systems Challenge 2026', 
    'Robotics & Embedded IoT', 
    'Premier robotics challenge hosted by IIT Bombay to design autonomous drones, ROS2 robotic navigation, and smart embedded sensor networks for precision agriculture.',
    'External', 'Hybrid', 'IIT Bombay & Regional Centers', 
    'IIT Bombay & Ministry of Education', 
    'Enrolled undergraduate engineering students.',
    'https://www.e-yantra.org', '2026-12-08', '2026-12-28', '2026-12-30', 
    2, 4, '₹2,50,000 + Paid Research Fellowships', 'Open', 1
),
(
    11, NULL, 
    'Google Solution Challenge 2026 – UN 17 Global Goals', 
    'Web & App Development', 
    'Invites university students to develop solutions for one or more of the United Nations 17 Sustainable Development Goals using Google Cloud, Flutter, and Android.',
    'External', 'Online', 'Google Developer Community Hub', 
    'Google Developer Student Clubs (GDSC)', 
    'Members of active GDSC chapters globally.',
    'https://developers.google.com/community/gdsc-solution-challenge', '2027-01-15', '2027-02-01', '2027-02-03', 
    1, 4, '$12,000 USD + Mentorship from Google Engineers', 'Open', 1
),
(
    12, NULL, 
    'Microsoft Imagine Cup 2026 – AI for Earth & Humanity', 
    'AI/ML & Generative AI', 
    'Global student technology competition providing an opportunity to build real-world AI and cloud applications on Microsoft Azure that solve critical societal challenges.',
    'External', 'Online', 'Microsoft Student Hub', 
    'Microsoft Global Student Programs', 
    'Students aged 16+ enrolled in high school or higher education.',
    'https://imaginecup.microsoft.com', '2027-01-20', '2027-02-10', '2027-02-12', 
    1, 4, '$100,000 USD Grand Prize + Azure Grants', 'Open', 1
),
(
    13, NULL, 
    'Flipkart GRiD 7.0 – Autonomous Robotics & Vision Challenge', 
    'Robotics & Embedded IoT', 
    'Engineering campus challenge focusing on automated optical packet sorting, robotic picking arm kinematics, and edge computer vision in dynamic warehouse logistics.',
    'External', 'Online', 'Unstop Assessment Portal', 
    'Flipkart Engineering & Unstop', 
    'B.Tech / B.E. students graduating in 2026, 2027, or 2028.',
    'https://unstop.com/competitions/flipkart-grid-70', '2026-11-26', '2026-12-04', '2026-12-06', 
    2, 3, '₹5,00,000 + Pre-Placement Interviews', 'Open', 1
),
(
    14, 1, 
    'MedTech Innovation Summit 2026 – Clinical AI Diagnostics', 
    'Healthcare & Telemedicine', 
    'Inter-disciplinary healthcare hackathon co-hosted with medical institutes to engineer AI diagnostics for radiology scans, ECG arrhythmia detectors, and ICU alerts.',
    'Internal', 'Hybrid', 'PICT Innovation Centre & BJ Medical', 
    'PICT Bio-Informatics Lab & Medical Board', 
    'Open to student engineering and medical research teams.',
    NULL, '2026-12-14', '2026-12-22', '2026-12-24', 
    2, 4, '₹50,000 + Clinical Trial Incubation', 'Open', 2
),
(
    15, NULL, 
    'Tata Crucible Hackathon 2026 – Industrial IoT & Smart Factory', 
    'Sustainability & CleanTech', 
    'Campus hackathon from the Tata Group to design predictive equipment maintenance models, energy dissipation dashboards, and IoT automated factory floor monitoring.',
    'External', 'Online', 'Tata Crucible Competition Hub', 
    'Tata Sons & Tata Technologies', 
    'Full-time engineering and management students in India.',
    'https://www.tatacrucible.com', '2026-12-18', '2027-01-08', '2027-01-10', 
    2, 4, '₹3,00,000 + Incubation Grants', 'Open', 1
),
(
    16, NULL, 
    'National Clean Water & River Conservation Hackathon', 
    'Sustainability & CleanTech', 
    'National technology challenge focused on low-cost IoT turbidity sensors, effluent discharge tracking, and hydrological flood forecasting models for river basins.',
    'External', 'Hybrid', 'NMCG Headquarters, New Delhi', 
    'National Mission for Clean Ganga & MoE', 
    'Students of technical institutions and environmental research labs.',
    'https://nmcg.nic.in', '2026-12-24', '2027-01-14', '2027-01-16', 
    3, 5, '₹2,00,000 + Government Implementation', 'Open', 1
),
(
    17, 1, 
    'Pune Smart Mobility & EV Telematics Hackathon', 
    'Smart Cities & Governance', 
    'Build smart battery management systems (BMS), EV charging grid load balancers, and GPS commuter trip optimization apps in collaboration with municipal corporations.',
    'Internal', 'Offline', 'PICT Campus Lab 4', 
    'Department of Information Technology, PICT', 
    'Undergraduate engineering students from Pune district.',
    NULL, '2026-12-02', '2026-12-08', '2026-12-09', 
    2, 4, '₹30,000 + Smart City Pilot Grant', 'Open', 2
),
(
    18, 3, 
    'CyberDefense BlueTeam CTF & Defensive Security Sprint', 
    'Cybersecurity & Digital Defense', 
    'Hands-on cyber defense event focusing on real-time intrusion detection system (IDS) tuning, memory buffer overflow patching, and SIEM security log analysis.',
    'Internal', 'Online', 'VJTI Cyber Range Portal', 
    'VJTI Center of Cyber Security', 
    'Open to all enrolled students with knowledge of Linux and networking.',
    NULL, '2026-12-12', '2026-12-19', '2026-12-20', 
    1, 3, '₹40,000 + OffSec Training Vouchers', 'Open', 1
),
(
    19, 2, 
    'DefiPulse Web3 & Zero-Knowledge Identity Hackathon', 
    'FinTech & Blockchain', 
    'Design decentralized credential verification, zk-SNARK privacy mechanisms for student transcripts, and peer-to-peer micro-lending smart contracts on EVM.',
    'Internal', 'Hybrid', 'COEP Blockchain Research Lab', 
    'COEP Blockchain Research Group', 
    'Students proficient in Solidity, Rust, and Web3 frameworks.',
    NULL, '2026-12-15', '2026-12-26', '2026-12-28', 
    2, 4, '₹50,000 + Grant Sponsorship', 'Open', 2
),
(
    20, NULL, 
    'AWS DeepRacer Autonomous Racing & Reinforcement Learning League', 
    'AI/ML & Generative AI', 
    'Train reinforcement learning agents, tune reward functions in simulation, and deploy optimal neural policy networks onto 1/18th scale robotic race cars.',
    'External', 'Online', 'AWS DeepRacer Student Console', 
    'Amazon Web Services (AWS)', 
    'Active university students with an AWS Educate account.',
    'https://aws.amazon.com/deepracer', '2026-12-05', '2026-12-15', '2026-12-17', 
    1, 3, '$10,000 AWS Credits + Trophies', 'Open', 1
),
(
    21, 2, 
    'Smart Agriculture & AgriTech Drone Telemetry Ideathon', 
    'Robotics & Embedded IoT', 
    'Deploy drone multispectral imagery analysis, soil NPK telemetry sensors, and automated irrigation controllers to empower rural farming cooperatives.',
    'Internal', 'Hybrid', 'COEP Agriculture Extension Center', 
    'COEP Department of Agriculture Engineering', 
    'Teams of 2 to 4 interdisciplinary engineering students.',
    NULL, '2026-12-20', '2027-01-05', '2027-01-07', 
    2, 4, '₹35,000 + Farmer Pilot Deployment', 'Open', 2
),
(
    22, NULL, 
    'OpenHealth EHR & Rural Telemedicine Hackathon', 
    'Healthcare & Telemedicine', 
    'Build patient health record synchronization tools compliant with Ayushman Bharat Digital Mission (ABDM) standards using FHIR protocols for primary health centers.',
    'External', 'Online', 'Ayushman Bharat ABDM Sandbox', 
    'National Health Authority (NHA) & Ayushman Bharat', 
    'Indian university students and healthcare software developers.',
    'https://abdm.gov.in', '2027-01-10', '2027-01-22', '2027-01-24', 
    2, 5, '₹3,00,000 + ABDM Sandbox Integration', 'Open', 1
),
(
    23, 1, 
    'Quantum Computing Algorithms Sprint 2026', 
    'Quantum & DeepTech', 
    'Implement quantum optimization circuits (QAOA), Grover search simulations, and variational quantum eigensolvers for cryptography and chemical modeling using Qiskit.',
    'Internal', 'Online', 'PICT HPC Quantum Simulator', 
    'PICT High Performance Computing Center', 
    'Students with strong foundations in linear algebra and Python.',
    NULL, '2027-01-05', '2027-01-18', '2027-01-20', 
    1, 3, '₹30,000 + Quantum Cloud Access', 'Open', 2
),
(
    24, NULL, 
    'GovTech Public Grievance AI Solver Sprint', 
    'Smart Cities & Governance', 
    'Build automated citizen grievance categorization, duplicate petition clustering, and sentiment analytics pipelines for state administrative portals.',
    'External', 'Online', 'MyGov India Innovation Portal', 
    'DARPG & MyGov India', 
    'All Indian citizens enrolled in higher education institutes.',
    'https://mygov.in', '2026-11-22', '2026-11-29', '2026-11-30', 
    2, 4, '₹1,50,000 + National MyGov Showcase', 'Open', 1
),
(
    25, 3, 
    'GreenData Center & Carbon Neutral Computing Challenge', 
    'Sustainability & CleanTech', 
    'Develop scheduling algorithms for energy-aware Kubernetes clusters, dynamic CPU frequency governors, and PUE thermal optimization tools for academic data centers.',
    'Internal', 'Offline', 'VJTI Green IT Facility', 
    'VJTI Sustainable Computing Initiative', 
    'Third and Final Year engineering students.',
    NULL, '2026-10-15', '2026-10-22', '2026-10-24', 
    2, 4, '₹25,000 + Merit Certificates', 'Completed', 1
),
(
    26, NULL, 
    'SpaceTech Satellite Data & Geospatial AI Hackathon', 
    'Quantum & DeepTech', 
    'Analyze multi-spectral satellite telemetry from Cartosat and Oceansat for deforestation mapping, urban sprawl monitoring, and drought forecasting using PyTorch & GeoPandas.',
    'External', 'Online', 'ISRO MOSDAC Space Portal', 
    'ISRO & IN-SPACe National Space Promotion', 
    'Students in Aerospace, CS, IT, and Geoinformatics.',
    'https://www.isro.gov.in', '2026-11-05', '2026-11-12', '2026-11-14', 
    2, 4, '₹2,50,000 + ISRO Nodal Center Visit', 'In Progress', 1
);

-- ----------------------------------------------------------------------------
-- 6. Seed Hackathon Registrations (Diverse status examples for tracking)
-- ----------------------------------------------------------------------------
INSERT INTO hackathon_registrations (hackathon_id, user_id, status) VALUES
(1, 6, 'Approved'),
(1, 7, 'Approved'),
(1, 8, 'Approved'),
(1, 9, 'Approved'),
(1, 10, 'Approved'),
(1, 11, 'Approved'),
(2, 6, 'Approved'),
(2, 8, 'Approved'),
(3, 6, 'Approved'),
(3, 7, 'Approved'),
(5, 6, 'Applied'),
(7, 6, 'Approved'),
(8, 6, 'Waitlisted'),
(11, 6, 'Approved'),
(14, 6, 'Rejected'),
(20, 6, 'Applied');

-- Seed Standard Criteria for All Hackathons (1 to 26)
INSERT INTO evaluation_criteria (hackathon_id, criteria_name, max_score, weight_pct)
SELECT h.hackathon_id, c.name, 25.00, 25.00
FROM hackathons h
CROSS JOIN (
    SELECT 'Innovation & Originality' AS name
    UNION ALL SELECT 'Feasibility & Practical Utility'
    UNION ALL SELECT 'Technical Execution & DB Design'
    UNION ALL SELECT 'UI/UX & Final Presentation'
) c
WHERE h.hackathon_id NOT IN (SELECT DISTINCT hackathon_id FROM evaluation_criteria);

-- ----------------------------------------------------------------------------
-- 7. Seed Teams
-- ----------------------------------------------------------------------------
INSERT INTO teams (team_id, hackathon_id, team_name, invitation_code, leader_user_id) VALUES
(1, 1, 'CodeCrafters', 'INNO-CRAFT1', 6),
(2, 1, 'NeuralNomads', 'INNO-NOMAD2', 9),
(3, 1, 'PixelPioneers', 'INNO-PIXEL3', 11);

-- ----------------------------------------------------------------------------
-- 8. Seed Team Members
-- ----------------------------------------------------------------------------
INSERT INTO team_members (team_id, user_id, role_in_team) VALUES
(1, 6, 'Leader & Full Stack Developer'),
(1, 7, 'AI/ML Engineer'),
(1, 8, 'Backend & Cloud Engineer'),
(2, 9, 'Leader & Mobile Developer'),
(2, 10, 'Embedded Systems Engineer'),
(3, 11, 'Leader & UI/UX Designer');

-- ----------------------------------------------------------------------------
-- 9. Seed Projects
-- ----------------------------------------------------------------------------
INSERT INTO projects (
    project_id, team_id, hackathon_id, title, abstract, 
    tech_stack, github_repo_url, documentation_url, demo_video_url, submission_status
) VALUES
(
    1, 1, 1, 
    'EduPulse – AI-Powered Institutional Analytics & Attendance Tracking', 
    'An automated end-to-end platform leveraging computer vision and database analytics to measure student engagement, monitor hackathon attendance, and generate real-time institutional metrics.',
    'Python, Flask, OpenCV, MySQL, Bootstrap 5, Chart.js',
    'https://github.com/AtharvHinge27/edupulse',
    'https://edupulse.docs.io/architecture',
    'https://youtube.com/watch?v=edupulse-demo',
    'Evaluated'
),
(
    2, 2, 1, 
    'AgriVision – Smart Drone & IoT Crop Health Monitor', 
    'Decentralized edge compute pipeline detecting leaf blight and soil moisture anomalies using lightweight deep neural networks and real-time telemetry streaming.',
    'Flutter, Python, TensorFlow Lite, ESP32, MySQL',
    'https://github.com/sneharao/agrivision',
    'https://agrivision.readthedocs.io',
    'https://youtube.com/watch?v=agrivision-demo',
    'Evaluated'
),
(
    3, 3, 1, 
    'CivicConnect – Hyperlocal Citizen Grievance Portal', 
    'A citizen-first responsive web application for reporting municipal infrastructure issues with automated ticket routing, geospatial tagging, and SMS notifications.',
    'HTML5, Bootstrap 5, JavaScript, Flask, MySQL',
    'https://github.com/kavitaiyer/civicconnect',
    'https://civicconnect.portal.io/docs',
    'https://youtube.com/watch?v=civicconnect-demo',
    'Submitted'
);

-- ----------------------------------------------------------------------------
-- 10. Seed Judge Assignments
-- ----------------------------------------------------------------------------
INSERT INTO judge_assignments (hackathon_id, judge_user_id) VALUES
(1, 4),
(1, 5),
(2, 4);

-- ----------------------------------------------------------------------------
-- 11. Seed Evaluation Criteria
-- ----------------------------------------------------------------------------
INSERT INTO evaluation_criteria (hackathon_id, criteria_name, max_score, weight_pct) VALUES
(1, 'Innovation & Originality', 25.00, 25.00),
(1, 'Feasibility & Practical Utility', 25.00, 25.00),
(1, 'Technical Execution & DB Design', 25.00, 25.00),
(1, 'UI/UX & Final Presentation', 25.00, 25.00);

-- ----------------------------------------------------------------------------
-- 12. Seed Evaluations
-- ----------------------------------------------------------------------------
INSERT INTO evaluations (
    evaluation_id, project_id, judge_user_id, 
    innovation_score, feasibility_score, technical_score, presentation_score, 
    total_score, feedback
) VALUES
(
    1, 1, 4, 
    23.50, 24.00, 24.50, 23.00, 
    95.00, 
    'Outstanding database normalization, clean Flask endpoints, and high practical utility for educational institutions.'
),
(
    2, 1, 5, 
    24.00, 23.50, 24.00, 24.50, 
    96.00, 
    'Excellent presentation and responsive UI. The ER model and multi-college tenant design are top tier.'
),
(
    3, 2, 4, 
    22.00, 21.50, 22.00, 22.50, 
    88.00, 
    'Very solid IoT implementation and good mobile interface. Need deeper security for device credentials.'
),
(
    4, 2, 5, 
    23.00, 22.00, 21.00, 23.00, 
    89.00, 
    'Commendable effort on edge ML model conversion and field testing.'
);

-- ----------------------------------------------------------------------------
-- 13. Seed Attendance Records
-- ----------------------------------------------------------------------------
INSERT INTO attendance (hackathon_id, user_id, check_in_time, attendance_status, marked_by) VALUES
(1, 6, '2026-11-25 09:00:00', 'Present', 2),
(1, 7, '2026-11-25 09:05:00', 'Present', 2),
(1, 8, '2026-11-25 09:12:00', 'Present', 2),
(1, 9, '2026-11-25 09:20:00', 'Present', 2),
(1, 10, '2026-11-25 09:22:00', 'Present', 2),
(1, 11, '2026-11-25 09:30:00', 'Present', 2);

-- ----------------------------------------------------------------------------
-- 14. Seed Certificates
-- ----------------------------------------------------------------------------
INSERT INTO certificates (
    certificate_id, certificate_code, user_id, hackathon_id, team_id, 
    certificate_type, issue_date, verified_count
) VALUES
(1, 'INNO-2026-WIN001', 6, 1, 1, 'Winner', '2026-11-28', 14),
(2, 'INNO-2026-WIN002', 7, 1, 1, 'Winner', '2026-11-28', 8),
(3, 'INNO-2026-WIN003', 8, 1, 1, 'Winner', '2026-11-28', 5),
(4, 'INNO-2026-RUN001', 9, 1, 2, '1st Runner Up', '2026-11-28', 6),
(5, 'INNO-2026-RUN002', 10, 1, 2, '1st Runner Up', '2026-11-28', 4),
(6, 'INNO-2026-PAR001', 11, 1, 3, 'Participation', '2026-11-28', 2);

-- ----------------------------------------------------------------------------
-- 15. Seed Notifications
-- ----------------------------------------------------------------------------
INSERT INTO notifications (user_id, title, message, link, is_read) VALUES
(6, 'Congratulations!', 'Team CodeCrafters won 1st Place in InnoHacks 2026.', '/certificates', FALSE),
(6, 'Certificate Available', 'Your Winner Certificate (INNO-2026-WIN001) is ready for download.', '/certificates', FALSE),
(9, 'Leaderboard Update', 'Evaluation complete! Team NeuralNomads ranked 2nd Place.', '/leaderboard', FALSE),
(11, 'Evaluation in Progress', 'Your project CivicConnect is currently under evaluation by the judges.', '/evaluations', TRUE);

-- ----------------------------------------------------------------------------
-- 16. Seed Audit Logs
-- ----------------------------------------------------------------------------
INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details) VALUES
(1, 'SYSTEM_INIT', 'system', NULL, 'InnoSphere normalized database seeded successfully'),
(2, 'CREATE_HACKATHON', 'hackathons', 1, 'Created internal hackathon: InnoHacks 2026'),
(6, 'CREATE_TEAM', 'teams', 1, 'Atharv Hinge created team CodeCrafters (INNO-CRAFT1)'),
(4, 'SUBMIT_EVALUATION', 'projects', 1, 'Judge Anand Sharma submitted evaluation for EduPulse (Score: 95.00)');
